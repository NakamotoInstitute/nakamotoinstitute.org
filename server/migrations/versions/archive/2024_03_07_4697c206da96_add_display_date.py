"""Add display_date

Revision ID: 4697c206da96
Revises: fe0bbac910a2
Create Date: 2024-03-07 21:57:49.200754

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "4697c206da96"
down_revision: str | None = "fe0bbac910a2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "document_translations", sa.Column("display_date", sa.String(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("document_translations", "display_date")
