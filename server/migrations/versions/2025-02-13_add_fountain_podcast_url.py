"""Add fountain podcast url

Revision ID: 4abcf6b66204
Revises: dc23d4808390
Create Date: 2025-02-13 02:28:11.900626

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4abcf6b66204"
down_revision: str | None = "dc23d4808390"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_index(op.f("ix_episodes_slug"), "episodes", ["slug"], unique=False)
    op.add_column("podcasts", sa.Column("fountain_url", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("podcasts", "fountain_url")
    op.drop_index(op.f("ix_episodes_slug"), table_name="episodes")
