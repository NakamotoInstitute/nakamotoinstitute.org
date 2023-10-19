import datetime
from typing import TYPE_CHECKING, List, Literal

from sqlalchemy import Boolean, Date, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sni.database import format_check, locale_check
from sni.extensions import db

if TYPE_CHECKING:
    from sni.models import Author, Translator

document_authors = db.Table(
    "document_authors",
    db.Column("document_id", db.Integer, db.ForeignKey("documents.id")),
    db.Column("author_id", db.Integer, db.ForeignKey("authors.id")),
)

document_translators = db.Table(
    "document_translators",
    db.Column(
        "document_translation_id", db.Integer, db.ForeignKey("document_translations.id")
    ),
    db.Column("translator_id", db.Integer, db.ForeignKey("translators.id")),
)

document_formats = db.Table(
    "document_document_formats",
    db.Column("document_format_id", db.Integer, db.ForeignKey("document_formats.id")),
    db.Column(
        "document_translation_id",
        db.Integer,
        db.ForeignKey("document_translations.id"),
    ),
)


class DocumentFormat(db.Model):
    __tablename__ = "document_formats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    format_type: Mapped[str] = mapped_column(
        String,
        db.CheckConstraint(
            f"format_type IN {format_check}",
            name="format_type",
        ),
        nullable=True,
    )
    documents: Mapped[List["DocumentTranslation"]] = relationship(
        secondary=document_formats, back_populates="formats"
    )


class Document(db.Model):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image: Mapped[str] = mapped_column(String, nullable=True)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    granularity: Mapped[Literal["DAY", "MONTH", "YEAR"]] = mapped_column(
        String, nullable=False
    )
    doctype: Mapped[str] = mapped_column(String, nullable=False)
    external: Mapped[str] = mapped_column(String, nullable=True)
    authors: Mapped[List["Author"]] = relationship(
        secondary=document_authors, back_populates="docs"
    )
    translations: Mapped[List["DocumentTranslation"]] = relationship(
        back_populates="document"
    )
    has_math: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f"<Document({self.id})>"


class DocumentTranslation(db.Model):
    __tablename__ = "document_translations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    locale: Mapped[str] = mapped_column(
        String,
        db.CheckConstraint(f"locale IN {locale_check}", name="locale"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    sort_title: Mapped[str] = mapped_column(String, nullable=True)
    display_title: Mapped[str] = mapped_column(String, nullable=True)
    subtitle: Mapped[str] = mapped_column(String, nullable=True)
    slug: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    image_alt: Mapped[str] = mapped_column(String, nullable=True)
    document_id: Mapped[int] = mapped_column(db.ForeignKey("documents.id"))
    document: Mapped[Document] = relationship(back_populates="translations")
    formats: Mapped[DocumentFormat] = relationship(
        secondary=document_formats, back_populates="documents"
    )
    translators: Mapped[List["Translator"]] = relationship(
        secondary=document_translators, back_populates="docs"
    )

    __table_args__ = (db.UniqueConstraint("document_id", "locale"),)

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
        return f"<DocumentTranslation(locale={self.locale};slug={self.slug})>"
