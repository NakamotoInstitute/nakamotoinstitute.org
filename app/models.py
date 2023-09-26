# from decimal import Decimal
import datetime
from typing import List

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


class Author(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    sort_name: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posts: Mapped[List["BlogPost"]] = relationship(back_populates="author")

    def __repr__(self) -> str:
        return f"<Author({self.slug})>"


class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image: Mapped[str] = mapped_column(String, nullable=True)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    added: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    original_url: Mapped[str] = mapped_column(String, nullable=True)
    original_site: Mapped[str] = mapped_column(String, nullable=True)
    author_id: Mapped[int] = mapped_column(db.ForeignKey("author.id"))
    author: Mapped["Author"] = relationship(back_populates="posts")
    translations: Mapped[List["BlogPostTranslation"]] = relationship(
        back_populates="blog_post"
    )

    def __repr__(self) -> str:
        return f"<BlogPost({self.id})>"


class BlogPostTranslation(db.Model):
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
    blog_post_id: Mapped[int] = mapped_column(db.ForeignKey("blog_post.id"))
    blog_post: Mapped["BlogPost"] = relationship(back_populates="translations")

    __table_args__ = (db.UniqueConstraint("blog_post_id", "language"),)

    def __repr__(self) -> str:
        return f"<BlogPostTranslation(language={self.language};slug={self.slug})>"
