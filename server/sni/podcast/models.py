import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from sni.extensions import db
from sni.shared.models import MarkdownContent


class Episode(MarkdownContent):
    __tablename__ = "episodes"

    id: Mapped[int] = mapped_column(
        Integer, db.ForeignKey("markdown_content.id"), primary_key=True
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    duration: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str] = mapped_column(String, nullable=False)
    notes: Mapped[str] = mapped_column(String, nullable=False)
    youtube_id: Mapped[str] = mapped_column(String, nullable=False)

    __mapper_args__ = {"polymorphic_identity": "episode"}

    def __repr__(self) -> str:
        return f"<Episode({self.slug})>"
