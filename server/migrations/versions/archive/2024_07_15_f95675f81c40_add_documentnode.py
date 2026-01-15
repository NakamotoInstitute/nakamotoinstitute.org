"""Add DocumentNode

Revision ID: f95675f81c40
Revises: 006948e4f251
Create Date: 2024-07-15 19:58:25.148463

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f95675f81c40"
down_revision: str | None = "006948e4f251"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "document_nodes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("nav_title", sa.String(), nullable=True),
        sa.Column("heading", sa.String(), nullable=True),
        sa.Column("subheading", sa.String(), nullable=True),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("file_content", sa.Text(), nullable=False),
        sa.Column("html_content", sa.Text(), nullable=False),
        sa.Column("document_translation_id", sa.Integer(), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["document_translation_id"],
            ["document_translations.id"],
            name=op.f(
                "fk_document_nodes_document_translation_id_document_translations"
            ),
        ),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["document_nodes.id"],
            name=op.f("fk_document_nodes_parent_id_document_nodes"),
        ),
        sa.UniqueConstraint("slug", name=op.f("uq_document_nodes_slug")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_document_nodes")),
    )


def downgrade() -> None:
    op.drop_table("document_nodes")
