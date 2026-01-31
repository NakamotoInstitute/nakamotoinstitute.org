"""Rename locales enum to locale

Revision ID: 7e477abbd00e
Revises: d0e9a4846f4f
Create Date: 2026-01-31 17:00:24.037065

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7e477abbd00e"
down_revision: str | None = "d0e9a4846f4f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("ALTER TYPE locales RENAME TO locale")


def downgrade() -> None:
    op.execute("ALTER TYPE locale RENAME TO locales")
