import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sni.extensions import db

if TYPE_CHECKING:
    from sni.models import Quote


class ForumThread(db.Model):
    __tablename__ = "forum_threads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)
    posts: Mapped[List["ForumPost"]] = relationship(back_populates="thread")

    def __repr__(self):
        return f"<ForumThread {self.title}>"


class ForumPost(db.Model):
    __tablename__ = "forum_posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    satoshi_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=True)
    url: Mapped[str] = mapped_column(String, nullable=False)
    subject: Mapped[str] = mapped_column(String, nullable=False)
    poster_name: Mapped[str] = mapped_column(String, nullable=False)
    poster_url: Mapped[str] = mapped_column(String, nullable=True)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    nested_level: Mapped[int] = mapped_column(
        Integer,
        db.CheckConstraint("nested_level >= 0", name="nested_level"),
        nullable=False,
    )
    source_id: Mapped[str] = mapped_column(String, nullable=False)
    thread_id: Mapped[int] = mapped_column(
        Integer, db.ForeignKey("forum_threads.id"), nullable=False
    )
    thread: Mapped[ForumThread] = relationship(back_populates="posts")
    quotes: Mapped[List["Quote"]] = relationship(back_populates="post")

    def __repr__(self):
        return f"<ForumPost {self.subject} - {self.source_id}>"
