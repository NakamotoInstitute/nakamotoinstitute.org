import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sni.database import Base

if TYPE_CHECKING:
    from sni.models.content import HTMLRenderableContent


class Episode(Base):
    __tablename__ = "episodes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content_id: Mapped[int] = mapped_column(ForeignKey("content.id"), unique=True)
    content: Mapped["HTMLRenderableContent"] = relationship(uselist=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    duration: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str] = mapped_column(String, nullable=False)
    notes: Mapped[str] = mapped_column(String, nullable=False)
    youtube_id: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self) -> str:
        return f"<Episode({self.slug})>"
