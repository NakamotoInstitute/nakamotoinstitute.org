import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sni.extensions import db

if TYPE_CHECKING:
    from sni.models import Quote


class EmailThread(db.Model):
    __tablename__ = "email_threads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)
    emails: Mapped[List["Email"]] = relationship(back_populates="thread")

    def __repr__(self):
        return f"<EmailThread {self.title}>"


class Email(db.Model):
    __tablename__ = "emails"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    satoshi_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=True)
    url: Mapped[str] = mapped_column(String, nullable=False)
    subject: Mapped[str] = mapped_column(String, nullable=False)
    sent_from: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    source_id: Mapped[str] = mapped_column(String, nullable=False)
    parent_id: Mapped[int] = mapped_column(
        Integer, db.ForeignKey("emails.id"), nullable=True
    )
    replies: Mapped[List["Email"]] = relationship(
        backref=db.backref("parent", remote_side=[id])
    )
    thread_id = mapped_column(
        Integer, db.ForeignKey("email_threads.id"), nullable=False
    )
    thread: Mapped[EmailThread] = relationship(back_populates="emails")
    quotes: Mapped[List["Quote"]] = relationship(back_populates="email")

    def __repr__(self):
        return f"<Email {self.subject} - {self.source_id}>"
