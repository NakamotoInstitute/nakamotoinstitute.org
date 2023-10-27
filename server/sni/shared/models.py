import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sni.extensions import db


class MarkdownContent(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    file_metadata_id: Mapped[int] = mapped_column(db.ForeignKey("file_metadata.id"))
    file_metadata: Mapped["FileMetadata"] = relationship(
        "FileMetadata",
        backref=db.backref(
            "markdown_content", uselist=False, cascade="all, delete-orphan"
        ),
    )
    content_type: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "markdown_content",
        "polymorphic_on": "content_type",
    }


class FileMetadata(db.Model):
    __tablename__ = "file_metadata"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    hash: Mapped[str] = mapped_column(String, nullable=False)
    last_modified: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
