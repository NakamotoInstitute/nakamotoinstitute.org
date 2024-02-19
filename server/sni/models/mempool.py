import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sni.config import settings
from sni.constants import Locales
from sni.database import Base
from sni.models.content import MarkdownContent

if TYPE_CHECKING:
    from sni.models.authors import Author
    from sni.models.translators import Translator

blog_post_authors = Table(
    "blog_post_authors",
    Base.metadata,
    Column("blog_post_id", Integer, ForeignKey("blog_posts.id")),
    Column("author_id", Integer, ForeignKey("authors.id")),
)


blog_post_translators = Table(
    "blog_post_translators",
    Base.metadata,
    Column(
        "blog_post_translation_id",
        Integer,
        ForeignKey("blog_post_translations.id"),
    ),
    Column("translator_id", Integer, ForeignKey("translators.id")),
)


class BlogPost(Base):
    __tablename__ = "blog_posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[int] = mapped_column(String, nullable=False)
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
    series: Mapped["BlogSeries"] = relationship(back_populates="blog_posts")
    series_id: Mapped[int] = mapped_column(ForeignKey("blog_series.id"), nullable=True)
    series_index: Mapped[int] = mapped_column(Integer, nullable=True)
    has_math: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    __table_args__ = (UniqueConstraint("series_id", "series_index"),)

    @property
    def image_url(self):
        if self.image:
            return f"{settings.CDN_BASE_URL}/img/mempool/{self.slug}/{self.image}"
        return None

    def __repr__(self) -> str:
        return f"<BlogPost({self.id})>"


class BlogPostTranslation(MarkdownContent):
    __tablename__ = "blog_post_translations"

    id: Mapped[int] = mapped_column(
        Integer, ForeignKey("markdown_content.id"), primary_key=True
    )
    locale: Mapped[Locales] = mapped_column(
        Enum(Locales, values_callable=lambda x: [e.value for e in x]), nullable=False
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, nullable=False)
    excerpt: Mapped[str] = mapped_column(Text, nullable=False)
    image_alt: Mapped[str] = mapped_column(String, nullable=True)
    translation_url: Mapped[str] = mapped_column(String, nullable=True)
    translation_site: Mapped[str] = mapped_column(String, nullable=True)
    translation_site_url: Mapped[str] = mapped_column(String, nullable=True)
    blog_post_id: Mapped[int] = mapped_column(ForeignKey("blog_posts.id"))
    blog_post: Mapped[BlogPost] = relationship(back_populates="translations")
    translators: Mapped[List["Translator"]] = relationship(
        secondary=blog_post_translators, back_populates="posts"
    )

    __mapper_args__ = {"polymorphic_identity": "blog_post"}

    __table_args__ = (UniqueConstraint("blog_post_id", "locale"),)

    @property
    def translations(self):
        return sorted(
            [
                translation
                for translation in self.blog_post.translations
                if translation != self
            ],
            key=lambda t: t.locale,
        )

    @property
    def series(self):
        if self.blog_post.series:
            return next(
                (
                    series_translation
                    for series_translation in self.blog_post.series.translations
                    if series_translation.locale == self.locale
                ),
                None,
            )
        return None

    def __repr__(self) -> str:
        return f"<BlogPostTranslation(locale={self.locale.value};slug={self.slug})>"


class BlogSeries(Base):
    __tablename__ = "blog_series"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chapter_title: Mapped[bool] = mapped_column(Boolean)
    blog_posts: Mapped[List["BlogPost"]] = relationship(back_populates="series")
    translations: Mapped[List["BlogSeriesTranslation"]] = relationship(
        back_populates="blog_series"
    )

    def __repr__(self) -> str:
        return f"<BlogSeries(id={self.id})>"


class BlogSeriesTranslation(MarkdownContent):
    __tablename__ = "blog_series_translations"

    id: Mapped[int] = mapped_column(
        Integer, ForeignKey("markdown_content.id"), primary_key=True
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    locale: Mapped[Locales] = mapped_column(
        Enum(Locales, values_callable=lambda x: [e.value for e in x]), nullable=False
    )
    blog_series_id: Mapped[int] = mapped_column(ForeignKey("blog_series.id"))
    blog_series: Mapped[BlogSeries] = relationship(back_populates="translations")

    __mapper_args__ = {"polymorphic_identity": "blog_series"}

    __table_args__ = (UniqueConstraint("blog_series_id", "locale"),)

    @property
    def translations(self):
        return sorted(
            [
                translation
                for translation in self.blog_series.translations
                if translation != self
            ],
            key=lambda t: t.locale,
        )

    def __repr__(self) -> str:
        return f"<BlogSeriesTranslation(slug={self.slug})>"
