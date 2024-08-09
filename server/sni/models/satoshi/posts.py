import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sni.database import Base
from sni.models.content import JSONFile

if TYPE_CHECKING:
    from sni.models.satoshi.quotes import Quote


class ForumThreadFile(JSONFile):
    threads: Mapped[List["ForumThread"]] = relationship(
        "ForumThread", back_populates="file"
    )

    __mapper_args__ = {
        "polymorphic_identity": "forum_threads",
    }


class ForumThread(Base):
    __tablename__ = "forum_threads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)
    posts: Mapped[List["ForumPost"]] = relationship(back_populates="thread")
    file_id: Mapped[int] = mapped_column(Integer, ForeignKey("json_files.id"))
    file: Mapped[ForumThreadFile] = relationship(
        "ForumThreadFile", back_populates="threads"
    )

    def __repr__(self):
        return f"<ForumThread {self.title}>"


class ForumPostFile(JSONFile):
    posts: Mapped[List["ForumPost"]] = relationship("ForumPost", back_populates="file")

    __mapper_args__ = {
        "polymorphic_identity": "forum_posts",
    }


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
    quotes: Mapped[List["Quote"]] = relationship(
        back_populates="post", cascade="all, delete-orphan"
    )
    file_id: Mapped[int] = mapped_column(Integer, ForeignKey("json_files.id"))
    file: Mapped[ForumPostFile] = relationship("ForumPostFile", back_populates="posts")

    def __repr__(self):
        return f"<ForumPost {self.subject} - {self.source_id}>"
