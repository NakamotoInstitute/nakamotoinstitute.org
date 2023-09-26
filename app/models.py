# from decimal import Decimal
import datetime
from typing import List, Literal

from sqlalchemy import Date, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db

ALLOWED_LANGUAGES = [
    "ar",
    "de",
    "en",
    "es",
    "fa",
    "fi",
    "fr",
    "he",
    "it",
    "pt",
    "ru",
    "zh",
]
language_check = ", ".join([f"'{lang}'" for lang in ALLOWED_LANGUAGES])
language_check = f"({language_check})"


document_authors = db.Table(
    "document_authors",
    db.Column("document_id", db.Integer, db.ForeignKey("documents.id")),
    db.Column("author_id", db.Integer, db.ForeignKey("authors.id")),
)

blog_post_authors = db.Table(
    "blog_post_authors",
    db.Column("blog_post_id", db.Integer, db.ForeignKey("blog_posts.id")),
    db.Column("author_id", db.Integer, db.ForeignKey("authors.id")),
)


class Author(db.Model):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    sort_name: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posts: Mapped[List["BlogPost"]] = relationship(
        secondary=blog_post_authors, back_populates="authors"
    )
    docs: Mapped[List["Document"]] = relationship(
        secondary=document_authors, back_populates="authors"
    )

    def __repr__(self) -> str:
        return f"<Author({self.slug})>"


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

    def __repr__(self) -> str:
        return f"<Document({self.id})>"


class DocumentTranslation(db.Model):
    __tablename__ = "document_translations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    language: Mapped[str] = mapped_column(
        String,
        db.CheckConstraint(f"language IN {language_check}", name="language"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    sortTitle: Mapped[str] = mapped_column(String, nullable=True)
    subtitle: Mapped[str] = mapped_column(String, nullable=True)
    slug: Mapped[str] = mapped_column(String, nullable=False)
    image_alt: Mapped[str] = mapped_column(String, nullable=True)
    document_id: Mapped[int] = mapped_column(db.ForeignKey("documents.id"))
    document: Mapped[Document] = relationship(back_populates="translations")

    __table_args__ = (db.UniqueConstraint("document_id", "language"),)

    @property
    def translations(self):
        return sorted(
            [
                translation
                for translation in self.document.translations
                if translation != self
            ],
            key=lambda t: t.language,
        )

    def __repr__(self) -> str:
        return f"<DocumentTranslation(language={self.language};slug={self.slug})>"


class BlogPost(db.Model):
    __tablename__ = "blog_posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image: Mapped[str] = mapped_column(String, nullable=True)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    added: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    original_url: Mapped[str] = mapped_column(String, nullable=True)
    original_site: Mapped[str] = mapped_column(String, nullable=True)
    authors: Mapped[List["Author"]] = relationship(
        secondary=blog_post_authors, back_populates="posts"
    )
    translations: Mapped[List["BlogPostTranslation"]] = relationship(
        back_populates="blog_post"
    )

    def __repr__(self) -> str:
        return f"<BlogPost({self.id})>"


class BlogPostTranslation(db.Model):
    __tablename__ = "blog_post_translations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    language: Mapped[str] = mapped_column(
        String,
        db.CheckConstraint(f"language IN {language_check}", name="language"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, nullable=False)
    excerpt: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    image_alt: Mapped[str] = mapped_column(String, nullable=True)
    translation_url: Mapped[str] = mapped_column(String, nullable=True)
    translation_site: Mapped[str] = mapped_column(String, nullable=True)
    translation_site_url: Mapped[str] = mapped_column(String, nullable=True)
    blog_post_id: Mapped[int] = mapped_column(db.ForeignKey("blog_posts.id"))
    blog_post: Mapped[BlogPost] = relationship(back_populates="translations")

    __table_args__ = (db.UniqueConstraint("blog_post_id", "language"),)

    @property
    def translations(self):
        return sorted(
            [
                translation
                for translation in self.blog_post.translations
                if translation != self
            ],
            key=lambda t: t.language,
        )

    def __repr__(self) -> str:
        return f"<BlogPostTranslation(language={self.language};slug={self.slug})>"
