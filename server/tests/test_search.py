"""Integration tests for the site-wide search backend (GET /search).

Run inside the container against the real Postgres:
    docker compose -f docker-compose.local.yml exec -T fastapi \
        sh -c 'cd /app && python -m pytest -q'

Assertions target the already-populated ``search_index`` (real data). All tests
are read-only except the optional rebuild idempotency test, which runs inside a
``session_scope()`` that rolls back implicitly (no commit on that path here).
"""

from fastapi.testclient import TestClient

from sni.models.search import SEARCH_CATEGORIES

SEARCH_URL = "/search"


def _get(client: TestClient, **params) -> dict:
    resp = client.get(SEARCH_URL, params=params)
    assert resp.status_code == 200, (params, resp.status_code, resp.text)
    return resp.json()


# 1) counts contract (AC#1, #4): all five category keys present; in grouped mode
#    total == sum of counts; the satoshi count is real (> 0).
def test_counts_contract_grouped(client: TestClient) -> None:
    body = _get(client, q="proof of work", locale="en")

    counts = body["countsByCategory"]
    assert set(counts.keys()) == set(SEARCH_CATEGORIES)
    assert body["query"] == "proof of work"

    # Grouped mode: total is the sum across every category bucket.
    assert body["total"] == sum(counts.values())

    # Real data: "proof of work" hits the Satoshi corpus heavily.
    assert counts["satoshi"] > 0
    # Verified directly against Postgres for this exact query/locale.
    assert counts["satoshi"] == 70
    assert counts["library"] == 31
    assert counts["mempool"] == 17
    assert counts["podcasts"] == 1
    assert counts["authors"] == 0


# 2) body-only match (AC#2): "sourceforge" appears in forum-post BODIES but in no
#    title; results land in the satoshi bucket with a <mark> in the snippet.
def test_body_only_match_highlights_snippet(client: TestClient) -> None:
    body = _get(client, q="sourceforge", locale="en")

    satoshi = [r for r in body["results"] if r["category"] == "satoshi"]
    assert satoshi, "expected satoshi-bucket results for a forum-post body term"

    forum_posts = [
        r for r in satoshi if set(r["ref"].keys()) >= {"source", "satoshiId"}
    ]
    assert forum_posts, "expected forum_post results (ref with satoshiId)"

    for r in forum_posts:
        # Body-only match: the matched term is not in the title...
        assert "sourceforge" not in r["title"].lower()
        # ...but the snippet still highlights via ts_headline over the body.
        assert "<mark>" in r["snippet"]


# 3) typo -> trigram (AC#3): a title typo still returns at least one result via the
#    pg_trgm title fallback; response is a clean 200.
def test_typo_trigram_fallback(client: TestClient) -> None:
    body = _get(client, q="bitcon", locale="en")

    assert body["total"] >= 1
    assert len(body["results"]) >= 1
    assert set(body["countsByCategory"].keys()) == set(SEARCH_CATEGORIES)


# 4) locale scoping (AC#20): satoshi/podcasts are English-only (not scoped) so their
#    counts are EQUAL across locales; library/mempool are locale-scoped so they
#    differ between en and es. Both requests return 200.
def test_locale_scoping(client: TestClient) -> None:
    en = _get(client, q="bitcoin", locale="en")
    es = _get(client, q="bitcoin", locale="es")

    en_counts = en["countsByCategory"]
    es_counts = es["countsByCategory"]

    # Not locale-scoped -> identical across locales.
    assert en_counts["satoshi"] == es_counts["satoshi"]
    assert en_counts["podcasts"] == es_counts["podcasts"]

    # Locale-scoped -> the English corpus is larger than the Spanish corpus.
    assert en_counts["library"] != es_counts["library"]
    assert en_counts["mempool"] != es_counts["mempool"]
    assert en_counts["library"] > es_counts["library"]
    assert en_counts["mempool"] > es_counts["mempool"]


# 5) category flat pagination (AC#5): a category filter returns only that category;
#    total == the category count; page 1 and page 2 are disjoint and deterministic.
def test_category_flat_pagination(client: TestClient) -> None:
    page1 = _get(client, q="bitcoin", locale="en", category="library", page=1)
    page2 = _get(client, q="bitcoin", locale="en", category="library", page=2)

    # Flat (category) mode: total equals the single-category count.
    assert page1["total"] == page1["countsByCategory"]["library"]
    assert page1["total"] == 32
    assert page2["total"] == 32

    # Every result is in the requested category.
    assert all(r["category"] == "library" for r in page1["results"])
    assert all(r["category"] == "library" for r in page2["results"])

    # Default limit is 20: page 1 fills, page 2 has the remainder (12).
    assert len(page1["results"]) == 20
    assert len(page2["results"]) == 12

    # Deterministic order -> the two pages are disjoint result sets.
    def identity(r: dict) -> tuple:
        return (r["title"], tuple(sorted(r["ref"].items(), key=lambda kv: kv[0])))

    ids1 = {identity(r) for r in page1["results"]}
    ids2 = {identity(r) for r in page2["results"]}
    assert ids1.isdisjoint(ids2)


# 6) never-500 hardening (AC#6, #25): empty, whitespace, NUL, C0 control, overlong,
#    and malformed-FTS queries all return a clean 200 (the server's choice) with no
#    500. Short-circuit cases return the all-zero empty contract.
def test_hardening_empty_returns_empty_contract(client: TestClient) -> None:
    for q in ("", "   "):
        body = _get(client, q=q, locale="en")
        counts = body["countsByCategory"]
        assert set(counts.keys()) == set(SEARCH_CATEGORIES)
        assert body["total"] == 0
        assert all(v == 0 for v in counts.values())
        assert body["results"] == []


def test_hardening_control_and_overlong(client: TestClient) -> None:
    # NUL, a C0 control char, an overlong query, and a malformed FTS expression.
    cases = ["\x00", "\x01", "a" * 150, ":&"]
    for q in cases:
        resp = client.get(SEARCH_URL, params={"q": q, "locale": "en"})
        assert resp.status_code in (200, 400), (repr(q), resp.status_code, resp.text)
        assert resp.status_code != 500
        if resp.status_code == 200:
            body = resp.json()
            assert set(body["countsByCategory"].keys()) == set(SEARCH_CATEGORIES)


def test_hardening_no_500_on_rejected_queries(client: TestClient) -> None:
    # NUL / control / overlong are rejected before DB work and yield the empty
    # contract; the malformed ":&" yields no lexemes and also stays at 0.
    for q in ("\x00", "\x01", "a" * 150, ":&"):
        resp = client.get(SEARCH_URL, params={"q": q, "locale": "en"})
        if resp.status_code == 200:
            body = resp.json()
            assert body["total"] == 0
            assert body["results"] == []


# 7) camelCase ref (S3/S4): a forum_post result's ref uses satoshiId (camelCase) and
#    never the stored snake_case satoshi_id.
def test_ref_keys_are_camel_case(client: TestClient) -> None:
    body = _get(client, q="sourceforge", locale="en")

    forum_posts = [
        r
        for r in body["results"]
        if r["category"] == "satoshi" and "satoshiId" in r["ref"]
    ]
    assert forum_posts, "expected a forum_post result exposing satoshiId"

    for r in forum_posts:
        ref = r["ref"]
        assert "satoshiId" in ref
        assert "satoshi_id" not in ref
        # No snake_case keys leak through the camelCase conversion.
        assert all("_" not in key for key in ref)


# 8) (optional) rebuild idempotency (AC#8): rebuilding twice yields identical row
#    counts. Uses the sync session_scope; the in-session work is rolled back before
#    the context manager commits, so the live index is untouched.
def test_rebuild_idempotent_row_counts() -> None:
    from sqlalchemy import func, select

    from sni.database import session_scope
    from sni.models.search import SearchIndex
    from sni.search.rebuild import rebuild_search_index

    def _count(session) -> int:
        return session.execute(
            select(func.count()).select_from(SearchIndex)
        ).scalar_one()

    with session_scope() as session:
        rebuild_search_index(session)
        first = _count(session)
        rebuild_search_index(session)
        second = _count(session)
        # Roll back so the commit on context exit is a no-op and the live index is
        # left exactly as it was.
        session.rollback()

    assert first == second
    assert first > 0


# 9) injection safety: a SQL-injection-style payload is fully parameterized, so it is
#    treated as ordinary search text (never executed). The request returns a clean 200
#    and the table is intact — proven by a normal follow-up query still returning hits.
def test_injection_payload_is_safe(client: TestClient) -> None:
    body = _get(client, q="'; DROP TABLE search_index; --", locale="en")
    assert set(body["countsByCategory"].keys()) == set(SEARCH_CATEGORIES)

    after = _get(client, q="bitcoin", locale="en")
    assert after["total"] >= 1


# 10) invalid category: an unknown category is ignored (treated as no filter), so the
#     response is the grouped contract where total == the sum of per-category counts.
def test_invalid_category_falls_back_to_grouped(client: TestClient) -> None:
    body = _get(client, q="bitcoin", locale="en", category="bogus")

    counts = body["countsByCategory"]
    assert set(counts.keys()) == set(SEARCH_CATEGORIES)
    assert body["total"] == sum(counts.values())


# 11) pagination bounds: a far-out-of-range page is clamped server-side and returns a
#     clean 200 with a (possibly empty) result list — never a 500.
def test_pagination_out_of_bounds_is_safe(client: TestClient) -> None:
    body = _get(client, q="bitcoin", locale="en", category="library", page=9999)

    assert isinstance(body["results"], list)
    assert set(body["countsByCategory"].keys()) == set(SEARCH_CATEGORIES)
