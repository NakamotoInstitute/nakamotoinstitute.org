"""add search index

Revision ID: a60a253cf340
Revises: 7e477abbd00e
Create Date: 2026-05-29 05:14:56.559687

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "a60a253cf340"
down_revision: str | None = "7e477abbd00e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # pg_trgm powers GIN(title gin_trgm_ops) + similarity() ranking. Idempotent.
    # NOTE: on managed Postgres this can require extension privileges.
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")

    op.create_table(
        "search_index",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("entity_type", sa.Text(), nullable=False),
        sa.Column("category", sa.Text(), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=False),
        # REUSE the existing "locale" enum. create_type=False => no CREATE TYPE.
        sa.Column(
            "locale",
            postgresql.ENUM(
                "ar",
                "de",
                "en",
                "es",
                "fa",
                "fi",
                "fr",
                "he",
                "it",
                "ko",
                "pt-br",
                "ru",
                "tr",
                "vi",
                "zh-cn",
                name="locale",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("is_locale_scoped", sa.Boolean(), nullable=False),
        sa.Column("source", sa.Text(), nullable=True),
        sa.Column("slug", sa.Text(), nullable=False, server_default=""),
        sa.Column(
            "ref_ids",
            postgresql.JSONB(),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("title", sa.Text(), nullable=False, server_default=""),
        sa.Column("subtitle", sa.Text(), nullable=False, server_default=""),
        sa.Column("excerpt", sa.Text(), nullable=False, server_default=""),
        sa.Column("body", sa.Text(), nullable=False, server_default=""),
        sa.Column("date", sa.Date(), nullable=True),
        sa.Column("weight", sa.Integer(), nullable=False, server_default="0"),
        # GENERATED ALWAYS AS (...) STORED — literal 'english' config, A/B/C/D.
        # unaccent() is deliberately excluded (STABLE, not IMMUTABLE -> illegal here).
        sa.Column(
            "search_vector",
            postgresql.TSVECTOR(),
            sa.Computed(
                "setweight(to_tsvector('english', coalesce(title, '')), 'A') || "
                "setweight(to_tsvector('english', coalesce(subtitle, '')), 'B') || "
                "setweight(to_tsvector('english', coalesce(excerpt, '')), 'C') || "
                "setweight(to_tsvector('english', coalesce(body, '')), 'D')",
                persisted=True,
            ),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_search_index")),
        sa.UniqueConstraint(
            "entity_type",
            "entity_id",
            "locale",
            name="uq_search_index_entity_type_entity_id_locale",
        ),
        sa.CheckConstraint(
            "category IN ('satoshi','library','mempool','authors','podcasts')",
            name=op.f("ck_search_index_category"),
        ),
        sa.CheckConstraint(
            "entity_type IN ('forum_post','email','quote','skeptic',"
            "'library_doc','library_node','mempool_post','mempool_series',"
            "'author','podcast','episode')",
            name=op.f("ck_search_index_entity_type"),
        ),
    )

    op.create_index(
        "ix_search_index_search_vector",
        "search_index",
        ["search_vector"],
        postgresql_using="gin",
    )
    op.create_index(
        "ix_search_index_title_trgm",
        "search_index",
        ["title"],
        postgresql_using="gin",
        postgresql_ops={"title": "gin_trgm_ops"},
    )
    op.create_index("ix_search_index_category", "search_index", ["category"])
    op.create_index("ix_search_index_locale", "search_index", ["locale"])


def downgrade() -> None:
    op.drop_index("ix_search_index_locale", table_name="search_index")
    op.drop_index("ix_search_index_category", table_name="search_index")
    op.drop_index("ix_search_index_title_trgm", table_name="search_index")
    op.drop_index("ix_search_index_search_vector", table_name="search_index")
    op.drop_table("search_index")
    # DO NOT drop pg_trgm (shared extension) and DO NOT drop the "locale" enum
    # (owned by the initial migration; create_type=False means we never owned it).
