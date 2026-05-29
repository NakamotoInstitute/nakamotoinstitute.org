from bs4 import BeautifulSoup
from sqlalchemy import delete, func, insert, select
from sqlalchemy.orm import Session, joinedload

from sni.models.authors import Author
from sni.models.content import HTMLRenderableContent
from sni.models.library import (
    Document,
    DocumentNode,
    DocumentTranslation,
    document_authors,
)
from sni.models.mempool import (
    BlogPost,
    BlogPostTranslation,
    BlogSeriesTranslation,
    blog_post_authors,
)
from sni.models.podcasts import Episode, Podcast
from sni.models.satoshi.emails import Email
from sni.models.satoshi.posts import ForumPost
from sni.models.satoshi.quotes import Quote
from sni.models.search import SearchIndex
from sni.models.skeptics import Skeptic

TITLE_MAX = 200  # truncation budget for synthetic titles (quotes)

INSERT_COLUMNS = (  # search_vector is GENERATED -> intentionally absent
    "entity_type",
    "category",
    "entity_id",
    "locale",
    "is_locale_scoped",
    "source",
    "slug",
    "ref_ids",
    "title",
    "subtitle",
    "excerpt",
    "body",
    "date",
    "weight",
)


def strip_html(value: str | None) -> str:
    """Rendered-HTML body -> plain text. BeautifulSoup is already a dep
    (server/sni/content/markdown/renderer.py). Collapses whitespace."""
    if not value:
        return ""
    return BeautifulSoup(value, "html.parser").get_text(separator=" ", strip=True)


def clean_text(value: str | None) -> str:
    """Plain-text columns (forum_posts.text, emails.text, quotes.text):
    strip + collapse internal whitespace; no HTML parsing."""
    if not value:
        return ""
    return " ".join(value.split())


def truncate(value: str, limit: int = TITLE_MAX) -> str:
    value = value.strip()
    return value if len(value) <= limit else value[: limit - 1].rstrip() + "…"


def _chunks(rows: list[dict], size: int):
    for i in range(0, len(rows), size):
        yield rows[i : i + size]


# (1) forum_post -- category satoshi, is_locale_scoped=False
def build_forum_posts(session: Session) -> list[dict]:
    stmt = (
        select(ForumPost)
        .options(joinedload(ForumPost.thread))
        .filter(ForumPost.satoshi_id.isnot(None))
    )
    rows: list[dict] = []
    for p in session.execute(stmt).scalars():
        rows.append(
            {
                "entity_type": "forum_post",
                "category": "satoshi",
                "entity_id": p.id,
                "locale": "en",
                "is_locale_scoped": False,
                "source": p.thread.source,
                "slug": "",
                "ref_ids": {"source": p.thread.source, "satoshi_id": p.satoshi_id},
                "title": clean_text(p.subject),
                "subtitle": clean_text(p.thread.title),
                "excerpt": "",
                "body": clean_text(p.text),
                "date": p.date.date() if p.date else None,
                "weight": 0,
            }
        )
    return rows


# (2) email -- category satoshi, is_locale_scoped=False
def build_emails(session: Session) -> list[dict]:
    stmt = (
        select(Email)
        .options(joinedload(Email.thread))
        .filter(Email.satoshi_id.isnot(None))
    )
    rows: list[dict] = []
    for e in session.execute(stmt).scalars():
        rows.append(
            {
                "entity_type": "email",
                "category": "satoshi",
                "entity_id": e.id,
                "locale": "en",
                "is_locale_scoped": False,
                "source": e.thread.source,
                "slug": "",
                "ref_ids": {"source": e.thread.source, "satoshi_id": e.satoshi_id},
                "title": clean_text(e.subject),
                "subtitle": clean_text(e.thread.title),
                "excerpt": "",
                "body": clean_text(e.text),
                "date": e.date.date() if e.date else None,
                "weight": 0,
            }
        )
    return rows


# (3) quote -- category satoshi, is_locale_scoped=False
def build_quotes(session: Session) -> list[dict]:
    stmt = select(Quote).options(
        joinedload(Quote.categories),
        joinedload(Quote.post).joinedload(ForumPost.thread),
        joinedload(Quote.email).joinedload(Email.thread),
    )
    rows: list[dict] = []
    for q in session.execute(stmt).scalars().unique():
        if q.whitepaper:
            source_type, ref = "whitepaper", {}
            subtitle = "Bitcoin whitepaper"
        elif q.post is not None:
            source_type = "post"
            ref = {
                "post_source": q.post.thread.source,
                "post_satoshi_id": q.post.satoshi_id,
            }
            subtitle = f"{q.post.thread.source} post"
        elif q.email is not None:
            source_type = "email"
            ref = {
                "email_source": q.email.thread.source,
                "email_satoshi_id": q.email.satoshi_id,
            }
            subtitle = f"{q.email.thread.source} email"
        else:
            continue

        body_text = clean_text(q.text)
        rows.append(
            {
                "entity_type": "quote",
                "category": "satoshi",
                "entity_id": q.id,
                "locale": "en",
                "is_locale_scoped": False,
                "source": source_type,
                "slug": "",
                "ref_ids": {
                    "quote_id": q.id,
                    "source_type": source_type,
                    "category_slugs": [c.slug for c in q.categories],
                    **ref,
                },
                "title": truncate(body_text),
                "subtitle": subtitle,
                "excerpt": "",
                "body": body_text,
                "date": None,
                "weight": 0,
            }
        )
    return rows


# (4) skeptic -- category satoshi, is_locale_scoped=False
def build_skeptics(session: Session) -> list[dict]:
    stmt = select(Skeptic)
    rows: list[dict] = []
    for s in session.execute(stmt).scalars():
        slug = f"{s.name_slug}-{s.date.isoformat()}"
        rows.append(
            {
                "entity_type": "skeptic",
                "category": "satoshi",
                "entity_id": s.id,
                "locale": "en",
                "is_locale_scoped": False,
                "source": s.source,
                "slug": slug,
                "ref_ids": {"slug": slug},
                "title": clean_text(s.name),
                "subtitle": clean_text(s.title),
                "excerpt": clean_text(s.article or ""),
                "body": strip_html(s.excerpt) or clean_text(f"{s.name} {s.title}"),
                "date": s.date,
                "weight": 0,
            }
        )
    return rows


# (5) library_doc -- category library, is_locale_scoped=True
def build_library_docs(session: Session) -> list[dict]:
    stmt = (
        select(DocumentTranslation)
        .join(DocumentTranslation.content.of_type(HTMLRenderableContent))
        .options(
            joinedload(DocumentTranslation.content.of_type(HTMLRenderableContent)),
            joinedload(DocumentTranslation.document),
        )
        .filter(func.length(func.trim(HTMLRenderableContent.html_content)) > 0)
    )
    rows: list[dict] = []
    for dt in session.execute(stmt).scalars():
        rows.append(
            {
                "entity_type": "library_doc",
                "category": "library",
                "entity_id": dt.id,
                "locale": dt.locale.value,
                "is_locale_scoped": True,
                "source": None,
                "slug": dt.slug,
                "ref_ids": {"slug": dt.slug, "locale": dt.locale.value},
                "title": clean_text(dt.title),
                "subtitle": clean_text(dt.subtitle or ""),
                "excerpt": clean_text(dt.display_title or ""),
                "body": strip_html(dt.content.html_content),
                "date": dt.document.date,
                "weight": 0,
            }
        )
    return rows


# (6) library_node -- category library, is_locale_scoped=True
def build_library_nodes(session: Session) -> list[dict]:
    stmt = (
        select(DocumentNode)
        .join(DocumentNode.document_translation)
        .options(
            joinedload(DocumentNode.document_translation).joinedload(
                DocumentTranslation.document
            )
        )
    )
    rows: list[dict] = []
    for n in session.execute(stmt).scalars():
        dt = n.document_translation
        rows.append(
            {
                "entity_type": "library_node",
                "category": "library",
                "entity_id": n.id,
                "locale": dt.locale.value,
                "is_locale_scoped": True,
                "source": None,
                "slug": n.slug,
                "ref_ids": {
                    "node_slug": n.slug,
                    "doc_slug": dt.slug,
                    "locale": dt.locale.value,
                },
                "title": clean_text(n.title or n.nav_title or ""),
                "subtitle": clean_text(n.heading or ""),
                "excerpt": clean_text(n.subheading or ""),
                "body": strip_html(n.html_content),
                "date": dt.document.date if dt.document else None,
                "weight": 0,
            }
        )
    return rows


# (7) mempool_post -- category mempool, is_locale_scoped=True
def build_mempool_posts(session: Session) -> list[dict]:
    stmt = (
        select(BlogPostTranslation)
        .join(BlogPostTranslation.content.of_type(HTMLRenderableContent))
        .options(
            joinedload(BlogPostTranslation.content.of_type(HTMLRenderableContent)),
            joinedload(BlogPostTranslation.blog_post),
        )
    )
    rows: list[dict] = []
    for bpt in session.execute(stmt).scalars():
        rows.append(
            {
                "entity_type": "mempool_post",
                "category": "mempool",
                "entity_id": bpt.id,
                "locale": bpt.locale.value,
                "is_locale_scoped": True,
                "source": None,
                "slug": bpt.slug,
                "ref_ids": {"slug": bpt.slug, "locale": bpt.locale.value},
                "title": clean_text(bpt.title),
                "subtitle": clean_text(bpt.subtitle or ""),
                "excerpt": clean_text(bpt.excerpt),
                "body": strip_html(bpt.content.html_content),
                "date": bpt.blog_post.date,
                "weight": 0,
            }
        )
    return rows


# (8) mempool_series -- category mempool, is_locale_scoped=True
def build_mempool_series(session: Session) -> list[dict]:
    stmt = select(BlogSeriesTranslation)
    rows: list[dict] = []
    for bst in session.execute(stmt).scalars():
        rows.append(
            {
                "entity_type": "mempool_series",
                "category": "mempool",
                "entity_id": bst.id,
                "locale": bst.locale.value,
                "is_locale_scoped": True,
                "source": None,
                "slug": bst.slug,
                "ref_ids": {"slug": bst.slug, "locale": bst.locale.value},
                "title": clean_text(bst.title),
                "subtitle": "",
                "excerpt": "",
                "body": "",
                "date": None,
                "weight": 0,
            }
        )
    return rows


# (9) author -- category authors, is_locale_scoped=True (per-available-locale)
def build_authors(session: Session) -> list[dict]:
    authors_stmt = (
        select(Author)
        .join(Author.content.of_type(HTMLRenderableContent))
        .options(joinedload(Author.content.of_type(HTMLRenderableContent)))
    )
    authors_by_id = {a.id: a for a in session.execute(authors_stmt).scalars()}

    doc_locales = (
        select(document_authors.c.author_id, DocumentTranslation.locale)
        .join(Document, Document.id == document_authors.c.document_id)
        .join(DocumentTranslation, DocumentTranslation.document_id == Document.id)
    )
    post_locales = (
        select(blog_post_authors.c.author_id, BlogPostTranslation.locale)
        .join(BlogPost, BlogPost.id == blog_post_authors.c.blog_post_id)
        .join(
            BlogPostTranslation,
            BlogPostTranslation.blog_post_id == BlogPost.id,
        )
    )
    available = doc_locales.union(post_locales).subquery()

    rows: list[dict] = []
    for author_id, locale in session.execute(select(available)):
        a = authors_by_id.get(author_id)
        if a is None:
            continue
        locale_value = locale.value if hasattr(locale, "value") else locale
        rows.append(
            {
                "entity_type": "author",
                "category": "authors",
                "entity_id": a.id,
                "locale": locale_value,
                "is_locale_scoped": True,
                "source": None,
                "slug": a.slug,
                "ref_ids": {"slug": a.slug, "locale": locale_value},
                "title": clean_text(a.name),
                "subtitle": clean_text(a.sort_name or ""),
                "excerpt": "",
                "body": strip_html(a.content.html_content),
                "date": None,
                "weight": 0,
            }
        )
    return rows


# (10) podcast -- category podcasts, is_locale_scoped=False
def build_podcasts(session: Session) -> list[dict]:
    stmt = (
        select(Podcast)
        .join(Podcast.content.of_type(HTMLRenderableContent))
        .options(joinedload(Podcast.content.of_type(HTMLRenderableContent)))
    )
    rows: list[dict] = []
    for p in session.execute(stmt).scalars():
        rows.append(
            {
                "entity_type": "podcast",
                "category": "podcasts",
                "entity_id": p.id,
                "locale": "en",
                "is_locale_scoped": False,
                "source": None,
                "slug": p.slug,
                "ref_ids": {"slug": p.slug},
                "title": clean_text(p.name),
                "subtitle": clean_text(p.description_short or ""),
                "excerpt": clean_text(p.summary or ""),
                "body": (
                    f"{clean_text(p.description)} {strip_html(p.content.html_content)}"
                ).strip(),
                "date": None,
                "weight": 0,
            }
        )
    return rows


# (11) episode -- category podcasts, is_locale_scoped=False
def build_episodes(session: Session) -> list[dict]:
    stmt = (
        select(Episode)
        .join(Episode.podcast)
        .join(Episode.content.of_type(HTMLRenderableContent))
        .options(
            joinedload(Episode.podcast),
            joinedload(Episode.content.of_type(HTMLRenderableContent)),
        )
    )
    rows: list[dict] = []
    for e in session.execute(stmt).scalars():
        rows.append(
            {
                "entity_type": "episode",
                "category": "podcasts",
                "entity_id": e.id,
                "locale": "en",
                "is_locale_scoped": False,
                "source": None,
                "slug": e.slug,
                "ref_ids": {"podcast_slug": e.podcast.slug, "episode_slug": e.slug},
                "title": clean_text(e.title),
                "subtitle": clean_text(e.podcast.name),
                "excerpt": clean_text(e.summary or ""),
                "body": (
                    f"{strip_html(e.content.html_content)} {clean_text(e.notes or '')}"
                ).strip(),
                "date": e.date.date() if e.date else None,
                "weight": 0,
            }
        )
    return rows


def rebuild_search_index(session: Session) -> None:
    rows: list[dict] = []
    rows += build_forum_posts(session)
    rows += build_emails(session)
    rows += build_quotes(session)
    rows += build_skeptics(session)
    rows += build_library_docs(session)
    rows += build_library_nodes(session)
    rows += build_mempool_posts(session)
    rows += build_mempool_series(session)
    rows += build_authors(session)
    rows += build_podcasts(session)
    rows += build_episodes(session)

    # DELETE + INSERT in the caller's transaction. MVCC: concurrent readers keep
    # seeing the prior committed index until this txn commits; on exception the
    # session_scope() rolls back and the prior index is untouched.
    session.execute(delete(SearchIndex))
    for chunk in _chunks(rows, 1000):
        session.execute(insert(SearchIndex), chunk)  # never sets search_vector
    # NO session.commit() here.
