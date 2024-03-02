"""Add canonical slugs

Revision ID: fe0bbac910a2
Revises: e6407295137f
Create Date: 2024-02-19 16:33:48.479115

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "fe0bbac910a2"
down_revision: Union[str, None] = "e6407295137f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Update blog_posts
    op.add_column("blog_posts", sa.Column("slug", sa.String(), nullable=True))
    blog_posts_table = sa.table(
        "blog_posts", sa.column("id", sa.Integer), sa.column("slug", sa.String())
    )

    blog_post_translations_table = sa.table(
        "blog_post_translations",
        sa.column("blog_post_id", sa.Integer),
        sa.column("locale", sa.Enum(name="locales")),
        sa.column("slug", sa.String()),
    )
    subquery = (
        sa.select(blog_post_translations_table.c.slug)
        .where(
            sa.and_(
                blog_post_translations_table.c.blog_post_id == blog_posts_table.c.id,
                blog_post_translations_table.c.locale == "en",
            )
        )
        .limit(1)
        .scalar_subquery()
    )
    update_stmt = blog_posts_table.update().values(slug=subquery)
    op.execute(update_stmt)
    op.alter_column("blog_posts", "slug", nullable=False)

    # Update documents
    op.add_column("documents", sa.Column("slug", sa.String(), nullable=True))
    documents_table = sa.table(
        "documents", sa.column("id", sa.Integer), sa.column("slug", sa.String())
    )

    document_translations_table = sa.table(
        "document_translations",
        sa.column("document_id", sa.Integer),
        sa.column("locale", sa.Enum(name="locales")),
        sa.column("slug", sa.String()),
    )
    subquery = (
        sa.select(document_translations_table.c.slug)
        .where(
            sa.and_(
                document_translations_table.c.document_id == documents_table.c.id,
                document_translations_table.c.locale == "en",
            )
        )
        .limit(1)
        .scalar_subquery()
    )
    update_stmt = documents_table.update().values(slug=subquery)
    op.execute(update_stmt)
    op.alter_column("documents", "slug", nullable=False)


def downgrade() -> None:
    op.drop_column("documents", "slug")
    op.drop_column("blog_posts", "slug")
