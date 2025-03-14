import datetime

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sni.database import Base
from sni.models.content import JSONContent


class Skeptic(Base):
    __tablename__ = "skeptics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    name_slug: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    article: Mapped[str] = mapped_column(String, nullable=True)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)
    excerpt: Mapped[str] = mapped_column(Text, nullable=True)
    link: Mapped[str] = mapped_column(String, nullable=False)
    media_embed: Mapped[str] = mapped_column(Text, nullable=True)
    twitter_screenshot: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    wayback_link: Mapped[str] = mapped_column(String, nullable=True)
    content_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("json_content.id", ondelete="CASCADE"), nullable=False
    )
    content: Mapped[JSONContent] = relationship("JSONContent")

    @property
    def slug(self):
        return f"{self.name_slug}-{self.date}"

    def __repr__(self) -> str:
        return f"<Skeptic({self.name_slug})"
