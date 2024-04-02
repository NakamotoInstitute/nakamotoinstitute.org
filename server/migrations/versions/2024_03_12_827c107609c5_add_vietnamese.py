"""Add vietnamese

Revision ID: 827c107609c5
Revises: 4697c206da96
Create Date: 2024-03-12 15:18:41.724280

"""

from typing import Sequence, Union

from alembic import op
from alembic_postgresql_enum import TableReference

revision: str = "827c107609c5"
down_revision: Union[str, None] = "4697c206da96"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.sync_enum_values(
        "public",
        "locales",
        [
            "ar",
            "de",
            "en",
            "es",
            "fa",
            "fi",
            "fr",
            "he",
            "it",
            "ko",
            "pt-br",
            "ru",
            "vi",
            "zh-cn",
        ],
        [
            TableReference(
                table_schema="public",
                table_name="document_translations",
                column_name="locale",
            ),
            TableReference(
                table_schema="public",
                table_name="blog_post_translations",
                column_name="locale",
            ),
            TableReference(
                table_schema="public",
                table_name="blog_series_translations",
                column_name="locale",
            ),
        ],
        enum_values_to_rename=[],
    )


def downgrade() -> None:
    op.sync_enum_values(
        "public",
        "locales",
        [
            "ar",
            "de",
            "en",
            "es",
            "fa",
            "fi",
            "fr",
            "he",
            "it",
            "ko",
            "pt-br",
            "ru",
            "zh-cn",
        ],
        [
            TableReference(
                table_schema="public",
                table_name="document_translations",
                column_name="locale",
            ),
            TableReference(
                table_schema="public",
                table_name="blog_post_translations",
                column_name="locale",
            ),
            TableReference(
                table_schema="public",
                table_name="blog_series_translations",
                column_name="locale",
            ),
        ],
        enum_values_to_rename=[],
    )
