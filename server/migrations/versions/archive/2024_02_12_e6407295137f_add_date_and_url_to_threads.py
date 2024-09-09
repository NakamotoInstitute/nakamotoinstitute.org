"""Add date and url to threads

Revision ID: e6407295137f
Revises: 7e4e641d9e17
Create Date: 2024-02-12 19:30:02.142862

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "e6407295137f"
down_revision: Union[str, None] = "7e4e641d9e17"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "email_threads",
        sa.Column(
            "date",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )
    op.add_column(
        "email_threads",
        sa.Column(
            "url",
            sa.String(),
            nullable=False,
            server_default=sa.text("'https://example.com'"),
        ),
    )
    op.add_column(
        "forum_threads",
        sa.Column(
            "date",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )
    op.add_column(
        "forum_threads",
        sa.Column(
            "url",
            sa.String(),
            nullable=False,
            server_default=sa.text("'https://example.com'"),
        ),
    )


def downgrade() -> None:
    op.drop_column("forum_threads", "url")
    op.drop_column("forum_threads", "date")
    op.drop_column("email_threads", "url")
    op.drop_column("email_threads", "date")
