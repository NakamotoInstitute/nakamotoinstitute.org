import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sni.database import Base
from sni.models.content import JSONFile

if TYPE_CHECKING:
    from sni.models.satoshi.quotes import Quote


class EmailThreadFile(JSONFile):
    threads: Mapped[List["EmailThread"]] = relationship(
        "EmailThread", back_populates="file"
    )

    __mapper_args__ = {
        "polymorphic_identity": "email_threads",
    }


class EmailThread(Base):
    __tablename__ = "email_threads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)
    emails: Mapped[List["Email"]] = relationship(
        back_populates="thread", lazy="selectin"
    )
    file_id: Mapped[int] = mapped_column(Integer, ForeignKey("json_files.id"))
    file: Mapped[EmailThreadFile] = relationship(
        "EmailThreadFile", back_populates="threads", lazy="selectin"
    )

    def __repr__(self):
        return f"<EmailThread {self.title}>"


class EmailFile(JSONFile):
    emails: Mapped[List["Email"]] = relationship(
        "Email", back_populates="file", lazy="selectin"
    )

    __mapper_args__ = {
        "polymorphic_identity": "emails",
    }


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
    parent_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("emails.id"), nullable=True
    )
    parent: Mapped["Email"] = relationship(
        "Email",
        back_populates="replies",
        remote_side=[id],
        lazy="joined",
    )
    replies: Mapped[List["Email"]] = relationship(
        "Email", back_populates="parent", lazy="selectin", join_depth=1
    )
    thread_id = mapped_column(Integer, ForeignKey("email_threads.id"), nullable=False)
    thread: Mapped[EmailThread] = relationship(back_populates="emails", lazy="joined")
    quotes: Mapped[List["Quote"]] = relationship(
        back_populates="email", lazy="selectin"
    )
    file_id: Mapped[int] = mapped_column(Integer, ForeignKey("json_files.id"))
    file: Mapped[EmailFile] = relationship(
        "EmailFile", back_populates="emails", lazy="selectin"
    )

    def __repr__(self):
        return f"<Email {self.subject} - {self.source_id}>"
