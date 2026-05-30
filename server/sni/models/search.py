from sqlalchemy import (
    CheckConstraint,
    Computed,
    Date,
    Index,
    Integer,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import ENUM, JSONB, TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column

from sni.constants import Locale
from sni.database import Base

# Categories: the public-facing search tabs.
SEARCH_CATEGORIES = ("satoshi", "library", "mempool", "authors", "podcasts")

# entity_type: the concrete source per row.
SEARCH_ENTITY_TYPES = (
    "forum_post",
    "email",
    "quote",
    "skeptic",
    "library_doc",
    "library_node",
    "mempool_post",
    "mempool_series",
    "author",
    "podcast",
    "episode",
)

# REUSE the pre-existing Postgres enum type. Its real name is "locale" (singular),
# after the 2026-01-31 rename (ALTER TYPE locales RENAME TO locale). Verified in the
# initial migration and every *_translations.locale column.
# create_type=False => Alembic/SQLAlchemy never re-emits CREATE TYPE.
locale_enum = ENUM(
    *(loc.value for loc in Locale),
    name="locale",
    create_type=False,
)

# search_vector is GENERATED ALWAYS AS (...) STORED with the literal 'english' config
# and A/B/C/D weights. Declared here as a read-only Computed column so reads work; the
# rebuild pipeline must NEVER write to it (Postgres rejects writes to GENERATED cols).
SEARCH_VECTOR_EXPR = (
    "setweight(to_tsvector('english', coalesce(title, '')), 'A') || "
    "setweight(to_tsvector('english', coalesce(subtitle, '')), 'B') || "
    "setweight(to_tsvector('english', coalesce(excerpt, '')), 'C') || "
    "setweight(to_tsvector('english', coalesce(body, '')), 'D')"
)


class SearchIndex(Base):
    __tablename__ = "search_index"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entity_type: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(Text, nullable=False)
    entity_id: Mapped[int] = mapped_column(Integer, nullable=False)
    locale: Mapped[str] = mapped_column(locale_enum, nullable=False)
    is_locale_scoped: Mapped[bool] = mapped_column(nullable=False)
    source: Mapped[str | None] = mapped_column(Text, nullable=True)
    slug: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    ref_ids: Mapped[dict] = mapped_column(
        JSONB, nullable=False, server_default=text("'{}'::jsonb")
    )
    title: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    subtitle: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    excerpt: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    body: Mapped[str] = mapped_column(Text, nullable=False, server_default="")
    date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    weight: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")

    # GENERATED ALWAYS AS (...) STORED. Read-only; never written by Python.
    search_vector: Mapped[str] = mapped_column(
        TSVECTOR,
        Computed(SEARCH_VECTOR_EXPR, persisted=True),
        nullable=True,
    )

    __table_args__ = (
        UniqueConstraint(
            "entity_type",
            "entity_id",
            "locale",
            name="uq_search_index_entity_type_entity_id_locale",
        ),
        CheckConstraint(
            "category IN ('satoshi','library','mempool','authors','podcasts')",
            name="ck_search_index_category",
        ),
        CheckConstraint(
            "entity_type IN ('forum_post','email','quote','skeptic',"
            "'library_doc','library_node','mempool_post','mempool_series',"
            "'author','podcast','episode')",
            name="ck_search_index_entity_type",
        ),
        Index("ix_search_index_search_vector", "search_vector", postgresql_using="gin"),
        Index(
            "ix_search_index_title_trgm",
            "title",
            postgresql_using="gin",
            postgresql_ops={"title": "gin_trgm_ops"},
        ),
        Index("ix_search_index_category", "category"),
        Index("ix_search_index_locale", "locale"),
    )

    def __repr__(self) -> str:
        return f"<SearchIndex({self.entity_type}:{self.entity_id}:{self.locale})>"
