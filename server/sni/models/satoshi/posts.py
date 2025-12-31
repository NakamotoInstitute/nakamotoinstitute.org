import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sni.database import Base
from sni.models.content import JSONContent

if TYPE_CHECKING:
    from sni.models.satoshi.quotes import Quote


class ForumThread(Base):
    __tablename__ = "forum_threads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)
    posts: Mapped[list["ForumPost"]] = relationship(back_populates="thread")
    content_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("json_content.id", ondelete="CASCADE"), nullable=False
    )
    content: Mapped[JSONContent] = relationship("JSONContent")

    def __repr__(self):
        return f"<ForumThread {self.title}>"


class ForumPost(Base):
    __tablename__ = "forum_posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    satoshi_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=True)
    url: Mapped[str] = mapped_column(String, nullable=False)
    subject: Mapped[str] = mapped_column(String, nullable=False)
    poster_name: Mapped[str] = mapped_column(String, nullable=False)
    poster_url: Mapped[str] = mapped_column(String, nullable=True)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    disclaimer: Mapped[str] = mapped_column(String, nullable=True)
    nested_level: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("nested_level >= 0", name="nested_level"),
        nullable=False,
    )
    source_id: Mapped[str] = mapped_column(String, nullable=False)
    thread_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("forum_threads.id"), nullable=False
    )
    thread: Mapped[ForumThread] = relationship(back_populates="posts")
    quotes: Mapped[list["Quote"]] = relationship(
        back_populates="post", cascade="all, delete-orphan"
    )
    content_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("json_content.id", ondelete="CASCADE"), nullable=False
    )
    content: Mapped[JSONContent] = relationship("JSONContent")

    def __repr__(self):
        return f"<ForumPost {self.subject} - {self.source_id}>"
