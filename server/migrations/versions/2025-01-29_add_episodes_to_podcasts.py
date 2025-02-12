"""Add episodes to podcasts

Revision ID: dc23d4808390
Revises: 6f5ac8890ba9
Create Date: 2025-01-29 22:27:08.677180

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "dc23d4808390"
down_revision: Union[str, None] = "6f5ac8890ba9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("episodes", sa.Column("podcast_id", sa.Integer(), nullable=True))
    op.alter_column("episodes", "notes", nullable=True)
    op.alter_column("episodes", "duration", nullable=True)
    op.alter_column("episodes", "youtube_id", nullable=True)
    op.add_column("episodes", sa.Column("episode_number", sa.Integer(), nullable=True))
    op.add_column("episodes", sa.Column("mp3_url", sa.String(), nullable=True))
    op.add_column("episodes", sa.Column("rumble_id", sa.String(), nullable=True))
    op.drop_constraint("uq_episodes_slug", "episodes", type_="unique")
    op.execute(
        "UPDATE file_metadata SET filename = REPLACE(filename, "
        "'content/podcast', 'content/podcast_episodes')"
        "WHERE id IN (SELECT content_id FROM episodes)"
    )
    op.execute(
        "UPDATE episodes SET podcast_id = ("
        "SELECT id FROM podcasts WHERE slug = 'the-crypto-mises-podcast'"
        ")"
    )
    op.alter_column("episodes", "podcast_id", nullable=False)
    op.create_unique_constraint(
        "uq_episodes_podcast_id_slug", "episodes", ["podcast_id", "slug"]
    )
    op.create_foreign_key(
        op.f("fk_episodes_podcast_id_podcasts"),
        "episodes",
        "podcasts",
        ["podcast_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("fk_episodes_podcast_id_podcasts"), "episodes", type_="foreignkey"
    )
    op.drop_constraint("uq_episodes_podcast_id_slug", "episodes", type_="unique")
    op.create_unique_constraint("uq_episodes_slug", "episodes", ["slug"])
    op.drop_column("episodes", "podcast_id")
