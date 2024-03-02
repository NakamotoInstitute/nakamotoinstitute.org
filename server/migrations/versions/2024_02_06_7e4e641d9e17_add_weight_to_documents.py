"""Add weight to documents

Revision ID: 7e4e641d9e17
Revises: c57f673dad76
Create Date: 2024-02-06 18:34:42.603434

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7e4e641d9e17"
down_revision: Union[str, None] = "c57f673dad76"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "yaml_files",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("file_metadata_id", sa.Integer(), nullable=False),
        sa.Column("content_type", sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(
            ["file_metadata_id"],
            ["file_metadata.id"],
            name=op.f("fk_yaml_files_file_metadata_id_file_metadata"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_yaml_files")),
    )
    op.add_column(
        "documents",
        sa.Column("weight", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    op.drop_column("documents", "weight")
    op.drop_table("yaml_files")
