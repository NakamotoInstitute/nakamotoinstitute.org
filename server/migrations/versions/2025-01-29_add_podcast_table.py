"""Add podcast table

Revision ID: 6f5ac8890ba9
Revises: 187b150943fc
Create Date: 2025-01-29 20:09:12.408344

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6f5ac8890ba9"
down_revision: Union[str, None] = "187b150943fc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "podcasts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content_id", sa.Integer(), nullable=False),
        sa.Column("defunct", sa.Boolean(), nullable=False, default=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("sort_name", sa.String(), nullable=True),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("description_short", sa.String(), nullable=True),
        sa.Column("summary", sa.String(), nullable=True),
        sa.Column("image_small", sa.String(), nullable=True),
        sa.Column("image_large", sa.String(), nullable=True),
        sa.Column("category", sa.String(), nullable=True),
        sa.Column("subcategory", sa.String(), nullable=True),
        sa.Column("external_feed", sa.String(), nullable=True),
        sa.Column("spotify_url", sa.String(), nullable=True),
        sa.Column("apple_podcasts_url", sa.String(), nullable=True),
        sa.Column("on_youtube", sa.Boolean(), nullable=False, default=False),
        sa.Column("on_rumble", sa.Boolean(), nullable=False, default=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_podcasts")),
        sa.ForeignKeyConstraint(
            ["content_id"], ["content.id"], name=op.f("fk_podcasts_content_id_content")
        ),
        sa.UniqueConstraint("content_id", name=op.f("uq_podcasts_content_id")),
        sa.UniqueConstraint("slug", name=op.f("uq_podcasts_slug")),
    )


def downgrade() -> None:
    op.drop_table("podcasts")
