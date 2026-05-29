import re
import unicodedata

from pydantic.alias_generators import to_camel
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from sni.constants import LocaleType
from sni.models.search import SEARCH_CATEGORIES

# S6 hardening caps (server-controlled).
MAX_QUERY_LENGTH = 100
PER_CAT = 5
MIN_LIMIT = 1
MAX_LIMIT = 50
DEFAULT_LIMIT = 20
MIN_PAGE = 1
MAX_PAGE = 200
MAX_OFFSET = 5000
SNIPPET_MAX_CHARS = 240

# C0/C1 control chars (NUL through US, DEL, and the C1 block) excluding normal
# whitespace (\t \n \r). Reject queries containing any of these before DB work.
_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")
_WHITESPACE = re.compile(r"\s+")

# The single unified CTE (S4). Both `page` rows and `counts` are wrapped in one
# json_build_object so the whole result is a single round trip computed once over
# `filtered`. Every value is a bound parameter (S6: parameterized only).
SEARCH_SQL = text(
    """
WITH q AS (
    SELECT websearch_to_tsquery('english', :q) AS query
),
filtered AS (
    SELECT s.*
    FROM search_index s, q
    WHERE (
            s.search_vector @@ q.query
            OR s.title % :q
          )
      AND (
            s.is_locale_scoped = false
            OR s.locale = cast(:locale AS locale)
          )
),
counts AS (
    SELECT category, count(*) AS n
    FROM filtered
    GROUP BY category
),
scored AS (
    SELECT f.*,
           GREATEST(
             ts_rank_cd(f.search_vector, q.query, 32),
             similarity(f.title, :q) * 0.25
           ) AS rank
    FROM filtered f, q
),
windowed AS (
    SELECT s.*,
           row_number() OVER (
             PARTITION BY s.category
             ORDER BY s.rank DESC, s.date DESC NULLS LAST, s.id
           ) AS rn
    FROM scored s
),
page AS (
    SELECT * FROM windowed
    WHERE (cast(:category AS text) IS NULL AND rn <= :per_cat)
       OR (cast(:category AS text) IS NOT NULL AND category = cast(:category AS text))
    ORDER BY
       CASE WHEN cast(:category AS text) IS NULL THEN category END,
       rank DESC, date DESC NULLS LAST, id
    LIMIT  CASE WHEN cast(:category AS text) IS NULL THEN NULL ELSE :limit END
    OFFSET CASE WHEN cast(:category AS text) IS NULL THEN 0    ELSE :offset END
),
results AS (
    SELECT
        p.entity_type, p.category, p.title, p.subtitle, p.excerpt, p.body,
        p.ref_ids, p.date, p.rank, p.slug, p.source,
        ts_headline(
            'english',
            coalesce(nullif(p.body, ''), p.excerpt),
            (SELECT query FROM q),
            'StartSel=<mark>, StopSel=</mark>, MaxFragments=2, MaxWords=30, '
            'MinWords=10, ShortWord=3'
        ) AS snippet
    FROM page p
    ORDER BY
        CASE WHEN cast(:category AS text) IS NULL THEN p.category END,
        p.rank DESC, p.date DESC NULLS LAST, p.id
)
SELECT json_build_object(
    'counts', coalesce(
        (SELECT json_object_agg(category, n) FROM counts), '{}'::json
    ),
    'results', coalesce(
        (SELECT json_agg(
            json_build_object(
                'entityType', r.entity_type,
                'category', r.category,
                'title', r.title,
                'subtitle', r.subtitle,
                'excerpt', r.excerpt,
                'body', r.body,
                'refIds', r.ref_ids,
                'source', r.source,
                'slug', r.slug,
                'date', r.date,
                'rank', r.rank,
                'snippet', r.snippet
            )
        ) FROM results r),
        '[]'::json
    )
) AS payload
"""
)


def _empty_response(query: str) -> dict:
    return {
        "query": query,
        "total": 0,
        "countsByCategory": {cat: 0 for cat in SEARCH_CATEGORIES},
        "results": [],
    }


def normalize_query(q: str) -> str | None:
    """Apply S6 normalization/charset rules.

    Returns the normalized query, or None if the query is rejected (overlong or
    containing NUL/control chars). An empty/whitespace-only query normalizes to "".
    """
    if q is None:
        return ""
    if len(q) > MAX_QUERY_LENGTH:
        return None
    if _CONTROL_CHARS.search(q):
        return None
    normalized = unicodedata.normalize("NFC", q)
    normalized = _WHITESPACE.sub(" ", normalized).strip()
    return normalized


def _clamp_pagination(page: int, limit: int) -> tuple[int, int]:
    limit = max(MIN_LIMIT, min(limit, MAX_LIMIT))
    page = max(MIN_PAGE, min(page, MAX_PAGE))
    offset = (page - 1) * limit
    offset = min(offset, MAX_OFFSET)
    return offset, limit


def _build_snippet(row: dict, q: str) -> str:
    """Python snippet fallback (S4 note).

    `ts_headline` returns empty markup for trigram-only title hits (no @@ match).
    When the headline has no <mark>, replace it with excerpt/subtitle/truncated body
    and wrap the matched title term so the frontend still highlights.
    """
    snippet = row.get("snippet") or ""
    if "<mark>" in snippet:
        return snippet

    fallback = (
        row.get("excerpt") or row.get("subtitle") or _truncate(row.get("body") or "")
    )
    return _highlight_title_term(fallback or row.get("title") or "", q)


def _truncate(body: str) -> str:
    body = _WHITESPACE.sub(" ", body).strip()
    if len(body) <= SNIPPET_MAX_CHARS:
        return body
    return body[:SNIPPET_MAX_CHARS].rstrip() + "…"


def _highlight_title_term(snippet: str, q: str) -> str:
    """Wrap the first query term found in the snippet with <mark> tags."""
    if not snippet or not q:
        return snippet
    for term in q.split():
        if len(term) < 2:
            continue
        match = re.search(re.escape(term), snippet, flags=re.IGNORECASE)
        if match:
            start, end = match.start(), match.end()
            return f"{snippet[:start]}<mark>{snippet[start:end]}</mark>{snippet[end:]}"
    return snippet


def _build_ref(row: dict) -> dict:
    """Merge the `source` column into the JSONB ref_ids map and camelCase the keys.

    The stored ref_ids JSONB uses snake_case keys (satoshi_id, doc_slug, …) but the
    frontend `searchResultHref` (S3) reads camelCase (satoshiId, docSlug, sourceType,
    postSatoshiId, …). Convert here so the API contract matches S3/S4.
    """
    ref: dict = dict(row.get("refIds") or {})
    source = row.get("source")
    if source is not None:
        ref["source"] = source
    return {to_camel(key): value for key, value in ref.items()}


async def search(
    *,
    db_session: AsyncSession,
    q: str,
    locale: LocaleType,
    category: str | None = None,
    page: int = 1,
) -> dict:
    """Execute the unified site-wide search (S4) with S6 hardening.

    Always returns the full response contract (counts for all five categories).
    Short-circuits with the empty contract on empty/no-lexeme queries (no DB hit).
    """
    normalized = normalize_query(q)
    if normalized is None:
        # Overlong / control-char query: return the empty contract cleanly.
        return _empty_response(q if q is not None else "")

    if normalized == "":
        return _empty_response(normalized)

    # Validate :category against SEARCH_CATEGORIES (or null) before binding.
    if category is not None and category not in SEARCH_CATEGORIES:
        category = None

    offset, limit = _clamp_pagination(page, DEFAULT_LIMIT)

    # numnode short-circuit: no lexemes => empty contract, no main query.
    numnode_row = await db_session.execute(
        text("SELECT numnode(websearch_to_tsquery('english', :q)) AS n").bindparams(
            q=normalized
        )
    )
    numnode = numnode_row.scalar_one()
    # No lexemes (a pure stopword/punctuation query) => empty contract, no main
    # query. Typos still tokenize to a lexeme (numnode >= 1), so the trigram title
    # fallback is unaffected; only no-op queries are short-circuited here.
    if numnode == 0:
        return _empty_response(normalized)

    # Statement timeout guards a pathological query (S6). SET LOCAL applies for the
    # current transaction.
    await db_session.execute(text("SET LOCAL statement_timeout = '3000ms'"))

    try:
        result = await db_session.execute(
            SEARCH_SQL.bindparams(
                q=normalized,
                locale=locale,
                category=category,
                limit=limit,
                offset=offset,
                per_cat=PER_CAT,
            )
        )
        payload = result.scalar_one()
    except DBAPIError:
        # statement_timeout (or any DB-level query cancel) degrades to the empty
        # contract rather than surfacing a 500; get_db() rolls the session back.
        return _empty_response(normalized)

    raw_counts = payload.get("counts") or {}
    counts_by_category = {cat: int(raw_counts.get(cat, 0)) for cat in SEARCH_CATEGORIES}

    if category is not None:
        total = counts_by_category.get(category, 0)
    else:
        total = sum(counts_by_category.values())

    results = []
    for row in payload.get("results") or []:
        results.append(
            {
                "entityType": row["entityType"],
                "category": row["category"],
                "title": row["title"],
                "snippet": _build_snippet(row, normalized),
                "ref": _build_ref(row),
                "date": row.get("date"),
                "rank": row["rank"],
            }
        )

    return {
        "query": normalized,
        "total": total,
        "countsByCategory": counts_by_category,
        "results": results,
    }
