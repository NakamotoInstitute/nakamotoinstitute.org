import datetime
from typing import TYPE_CHECKING, List, Literal

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sni.config import settings
from sni.constants import DocumentFormats, Locales
from sni.database import Base
from sni.models.content import MarkdownContent, YAMLFile

if TYPE_CHECKING:
    from sni.models.authors import Author
    from sni.models.translators import Translator

document_authors = Table(
    "document_authors",
    Base.metadata,
    Column("document_id", Integer, ForeignKey("documents.id")),
    Column("author_id", Integer, ForeignKey("authors.id")),
)

document_translators = Table(
    "document_translators",
    Base.metadata,
    Column("document_translation_id", Integer, ForeignKey("document_translations.id")),
    Column("translator_id", Integer, ForeignKey("translators.id")),
)

document_formats = Table(
    "document_document_formats",
    Base.metadata,
    Column("document_format_id", Integer, ForeignKey("document_formats.id")),
    Column(
        "document_translation_id",
        Integer,
        ForeignKey("document_translations.id"),
    ),
)


class DocumentFormat(Base):
    __tablename__ = "document_formats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    format_type: Mapped[str] = mapped_column(
        Enum(DocumentFormats, values_callable=lambda x: [e.value for e in x]),
        unique=True,
    )
    documents: Mapped[List["DocumentTranslation"]] = relationship(
        secondary=document_formats, back_populates="formats"
    )


class LibraryWeightFile(YAMLFile):
    __mapper_args__ = {
        "polymorphic_identity": "library_weights",
    }


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String, nullable=False)
    image: Mapped[str] = mapped_column(String, nullable=True)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    granularity: Mapped[Literal["DAY", "MONTH", "YEAR"]] = mapped_column(
        String, nullable=False
    )
    doctype: Mapped[str] = mapped_column(String, nullable=False)
    authors: Mapped[List["Author"]] = relationship(
        secondary=document_authors, back_populates="docs"
    )
    translations: Mapped[List["DocumentTranslation"]] = relationship(
        back_populates="document"
    )
    has_math: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    weight: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    @property
    def image_url(self):
        if self.image:
            return f"{settings.CDN_BASE_URL}/img/library/{self.slug}/{self.image}"
        return None

    def __repr__(self) -> str:
        return f"<Document({self.id})>"


class DocumentTranslation(MarkdownContent):
    __tablename__ = "document_translations"

    id: Mapped[int] = mapped_column(
        Integer, ForeignKey("markdown_content.id"), primary_key=True
    )
    locale: Mapped[Locales] = mapped_column(
        Enum(Locales, values_callable=lambda x: [e.value for e in x]), nullable=False
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    sort_title: Mapped[str] = mapped_column(String, nullable=True)
    display_title: Mapped[str] = mapped_column(String, nullable=True)
    subtitle: Mapped[str] = mapped_column(String, nullable=True)
    slug: Mapped[str] = mapped_column(String, nullable=False)
    external: Mapped[str] = mapped_column(String, nullable=True)
    image_alt: Mapped[str] = mapped_column(String, nullable=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
    document: Mapped[Document] = relationship(back_populates="translations")
    formats: Mapped[List[DocumentFormat]] = relationship(
        secondary=document_formats, back_populates="documents"
    )
    translators: Mapped[List["Translator"]] = relationship(
        secondary=document_translators, back_populates="docs"
    )

    __mapper_args__ = {"polymorphic_identity": "document"}

    __table_args__ = (UniqueConstraint("document_id", "locale"),)

    @property
    def translations(self):
        return sorted(
            [
                translation
                for translation in self.document.translations
                if translation != self
            ],
            key=lambda t: t.locale,
        )

    def __repr__(self) -> str:
        return f"<DocumentTranslation(locale={self.locale.value};slug={self.slug})>"
