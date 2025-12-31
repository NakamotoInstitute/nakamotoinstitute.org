import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sni.database import Base
from sni.models.content import JSONContent

if TYPE_CHECKING:
    from sni.models.satoshi.quotes import Quote


class EmailThread(Base):
    __tablename__ = "email_threads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)
    emails: Mapped[list["Email"]] = relationship(back_populates="thread")
    content_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("json_content.id", ondelete="CASCADE"), nullable=False
    )
    content: Mapped[JSONContent] = relationship("JSONContent")

    def __repr__(self):
        return f"<EmailThread {self.title}>"


class Email(Base):
    __tablename__ = "emails"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    satoshi_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=True)
    url: Mapped[str] = mapped_column(String, nullable=False)
    subject: Mapped[str] = mapped_column(String, nullable=False)
    sent_from: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    source_id: Mapped[str] = mapped_column(String, nullable=False)
    disclaimer: Mapped[str] = mapped_column(String, nullable=True)
    parent_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("emails.id"), nullable=True
    )
    parent: Mapped["Email"] = relationship(
        "Email",
        back_populates="replies",
        remote_side=[id],
        lazy="joined",
    )
    replies: Mapped[list["Email"]] = relationship(
        "Email", back_populates="parent", join_depth=1
    )
    thread_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("email_threads.id"), nullable=False
    )
    thread: Mapped[EmailThread] = relationship(back_populates="emails")
    quotes: Mapped[list["Quote"]] = relationship(
        back_populates="email", cascade="all, delete-orphan"
    )
    content_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("json_content.id", ondelete="CASCADE"), nullable=False
    )
    content: Mapped[JSONContent] = relationship("JSONContent")

    def __repr__(self):
        return f"<Email {self.subject} - {self.source_id}>"
