import datetime
from typing import ClassVar

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sni.database import Base


class Content(Base):
    __tablename__ = "content"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    file_content: Mapped[str] = mapped_column(Text, nullable=False)
    file_metadata_id: Mapped[int] = mapped_column(
        ForeignKey("file_metadata.id"), nullable=False, unique=True
    )
    file_metadata: Mapped["FileMetadata"] = relationship(
        "FileMetadata",
        back_populates="content",
        uselist=False,
    )
    content_type: Mapped[str] = mapped_column(String(50))

    __mapper_args__: ClassVar[dict] = {
        "polymorphic_identity": "content",
        "polymorphic_on": "content_type",
    }


class HTMLRenderableContent(Content):
    __tablename__ = "html_renderable_content"

    id: Mapped[int] = mapped_column(ForeignKey("content.id"), primary_key=True)
    html_content: Mapped[str] = mapped_column(Text, nullable=False)

    __mapper_args__: ClassVar[dict] = {
        "polymorphic_identity": "html_renderable_content",
    }


class MarkdownContent(HTMLRenderableContent):
    __tablename__ = "markdown_content"

    id: Mapped[int] = mapped_column(
        ForeignKey("html_renderable_content.id"), primary_key=True
    )

    __mapper_args__: ClassVar[dict] = {"polymorphic_identity": "markdown"}


class JSONContent(Content):
    __tablename__ = "json_content"

    id: Mapped[int] = mapped_column(ForeignKey("content.id"), primary_key=True)

    __mapper_args__: ClassVar[dict] = {"polymorphic_identity": "json"}


class YAMLContent(Content):
    __tablename__ = "yaml_content"

    id: Mapped[int] = mapped_column(ForeignKey("content.id"), primary_key=True)

    __mapper_args__: ClassVar[dict] = {"polymorphic_identity": "yaml"}


class FileMetadata(Base):
    __tablename__ = "file_metadata"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    hash: Mapped[str] = mapped_column(String, nullable=False)
    last_modified: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    content: Mapped["Content"] = relationship(
        "Content",
        back_populates="file_metadata",
        uselist=False,
        cascade="all, delete-orphan",
    )
