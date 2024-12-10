"""Add mempool subtitle

Revision ID: 187b150943fc
Revises: b0e886699202
Create Date: 2024-12-10 17:58:32.509185

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "187b150943fc"
down_revision: Union[str, None] = "b0e886699202"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "blog_post_translations", sa.Column("subtitle", sa.String(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("blog_post_translations", "subtitle")
