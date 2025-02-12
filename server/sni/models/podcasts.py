import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sni.database import Base

if TYPE_CHECKING:
    from sni.models.content import HTMLRenderableContent


class Podcast(Base):
    __tablename__ = "podcasts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    sort_name: Mapped[str] = mapped_column(String, nullable=True)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    defunct: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    content_id: Mapped[int] = mapped_column(ForeignKey("content.id"), unique=True)
    content: Mapped["HTMLRenderableContent"] = relationship(uselist=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    description_short: Mapped[str] = mapped_column(String, nullable=True)
    summary: Mapped[str] = mapped_column(String, nullable=True)
    image_small: Mapped[str] = mapped_column(String, nullable=True)
    image_large: Mapped[str] = mapped_column(String, nullable=True)
    category: Mapped[str] = mapped_column(String, nullable=True)
    subcategory: Mapped[str] = mapped_column(String, nullable=True)
    external_feed: Mapped[str] = mapped_column(String, nullable=True)
    spotify_url: Mapped[str] = mapped_column(String, nullable=True)
    apple_podcasts_url: Mapped[str] = mapped_column(String, nullable=True)
    on_youtube: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    on_rumble: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    episodes: Mapped[list["Episode"]] = relationship(
        back_populates="podcast", order_by="Episode.date.desc()"
    )

    def __repr__(self) -> str:
        return f"<Podcast({self.slug})>"


class Episode(Base):
    __tablename__ = "episodes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    podcast_id: Mapped[int] = mapped_column(ForeignKey("podcasts.id"))
    podcast: Mapped[Podcast] = relationship(back_populates="episodes")
    content_id: Mapped[int] = mapped_column(ForeignKey("content.id"), unique=True)
    content: Mapped["HTMLRenderableContent"] = relationship(uselist=False)
    episode_number: Mapped[int] = mapped_column(Integer, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, nullable=False, index=True)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    duration: Mapped[str] = mapped_column(String, nullable=True)
    summary: Mapped[str] = mapped_column(String, nullable=False)
    notes: Mapped[str] = mapped_column(String, nullable=True)
    mp3_url: Mapped[str] = mapped_column(String, nullable=True)
    youtube_id: Mapped[str] = mapped_column(String, nullable=True)
    rumble_id: Mapped[str] = mapped_column(String, nullable=True)

    __table_args__ = (
        UniqueConstraint("podcast_id", "slug", name="uq_episodes_podcast_id_slug"),
    )

    def __repr__(self) -> str:
        return f"<Episode({self.podcast.slug}/{self.slug})>"
