"""Add purchase link

Revision ID: a83ae97da366
Revises: f95675f81c40
Create Date: 2024-07-26 01:24:53.357004

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a83ae97da366"
down_revision: str | None = "f95675f81c40"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("documents", sa.Column("purchase_link", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("documents", "purchase_link")
