import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship

from sni.database import Base


class MarkdownContent(Base):
    __tablename__ = "markdown_content"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    file_content: Mapped[str] = mapped_column(Text, nullable=False)
    html_content: Mapped[str] = mapped_column(Text, nullable=False)
    file_metadata_id: Mapped[int] = mapped_column(ForeignKey("file_metadata.id"))
    file_metadata: Mapped["FileMetadata"] = relationship(
        "FileMetadata",
        backref=backref(
            "markdown_content", uselist=False, cascade="all, delete-orphan"
        ),
    )
    content_type: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "markdown_content",
        "polymorphic_on": "content_type",
    }


class JSONFile(Base):
    __tablename__ = "json_files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    file_metadata_id: Mapped[int] = mapped_column(ForeignKey("file_metadata.id"))
    file_metadata: Mapped["FileMetadata"] = relationship(
        "FileMetadata",
        backref=backref("json_files", uselist=False, cascade="all, delete-orphan"),
    )
    content_type: Mapped[str] = mapped_column(String(50))
    __mapper_args__ = {
        "polymorphic_identity": "json_file",
        "polymorphic_on": "content_type",
    }


class FileMetadata(Base):
    __tablename__ = "file_metadata"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    hash: Mapped[str] = mapped_column(String, nullable=False)
    last_modified: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
