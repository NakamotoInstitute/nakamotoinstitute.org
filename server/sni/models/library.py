import datetime
from functools import cached_property
from typing import TYPE_CHECKING, Self

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
from sni.constants import DocumentFormats, Granularity, Locale
from sni.database import Base

if TYPE_CHECKING:
    from sni.models.authors import Author
    from sni.models.content import HTMLRenderableContent
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
    )
    volume: Mapped[int | None] = mapped_column(Integer, nullable=True)
    documents: Mapped[list["DocumentTranslation"]] = relationship(
        secondary=document_formats, back_populates="formats"
    )

    __table_args__ = (UniqueConstraint("format_type", "volume"),)


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String, nullable=False)
    image: Mapped[str] = mapped_column(String, nullable=True)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    granularity: Mapped[Granularity] = mapped_column(String, nullable=False)
    doctype: Mapped[str] = mapped_column(String, nullable=False)
    authors: Mapped[list["Author"]] = relationship(
        secondary=document_authors, back_populates="docs"
    )
    translations: Mapped[list["DocumentTranslation"]] = relationship(
        back_populates="document"
    )
    has_math: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    weight: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    purchase_link: Mapped[str] = mapped_column(String, nullable=True)

    @property
    def image_url(self):
        if self.image:
            return f"{settings.CDN_BASE_URL}/img/library/{self.slug}/{self.image}"
        return None

    def __repr__(self) -> str:
        return f"<Document({self.id})>"


class DocumentTranslation(Base):
    __tablename__ = "document_translations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content_id: Mapped[int] = mapped_column(ForeignKey("content.id"), unique=True)
    content: Mapped["HTMLRenderableContent"] = relationship(uselist=False)
    locale: Mapped[Locale] = mapped_column(
        Enum(Locale, values_callable=lambda x: [e.value for e in x]), nullable=False
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    sort_title: Mapped[str] = mapped_column(String, nullable=True)
    display_title: Mapped[str] = mapped_column(String, nullable=True)
    display_date: Mapped[str] = mapped_column(String, nullable=True)
    subtitle: Mapped[str] = mapped_column(String, nullable=True)
    slug: Mapped[str] = mapped_column(String, nullable=False)
    external: Mapped[str] = mapped_column(String, nullable=True)
    image_alt: Mapped[str] = mapped_column(String, nullable=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
    document: Mapped[Document] = relationship(back_populates="translations")
    formats: Mapped[list[DocumentFormat]] = relationship(
        secondary=document_formats, back_populates="documents"
    )
    translators: Mapped[list["Translator"]] = relationship(
        secondary=document_translators, back_populates="docs"
    )
    nodes: Mapped[list["DocumentNode"]] = relationship(
        "DocumentNode", back_populates="document_translation"
    )

    __table_args__ = (UniqueConstraint("document_id", "locale"),)

    @property
    def serialized_formats(self) -> list[dict]:
        serialized_formats = []
        for fmt in self.formats:
            if self.slug == self.document.slug and self.locale != Locale.ENGLISH:
                slug = f"{self.slug}_{self.locale.value}"
            else:
                slug = self.slug

            format_type = fmt.format_type.value
            if fmt.volume is not None:
                filename = (
                    f"{settings.CDN_BASE_URL}/docs/{slug}_vol{fmt.volume}.{format_type}"
                )
            else:
                filename = f"{settings.CDN_BASE_URL}/docs/{slug}.{format_type}"

            serialized_formats.append(
                {"url": filename, "type": format_type, "volume": fmt.volume}
            )
        return sorted(serialized_formats, key=lambda x: (x["type"], x.get("volume", 0)))

    @property
    def translations(self) -> list[Self]:
        return sorted(
            [
                translation
                for translation in self.document.translations
                if translation != self
            ],
            key=lambda t: t.locale,
        )

    @cached_property
    def flattened_nodes(self):
        def _flatten(node, all_nodes):
            result = [node]
            children = sorted(
                (n for n in all_nodes if n.parent == node), key=lambda n: n.order
            )
            for child in children:
                result.extend(_flatten(child, all_nodes))
            return result

        top_level_nodes = sorted(
            (node for node in self.nodes if node.parent is None), key=lambda n: n.order
        )

        _flattened_nodes = []
        for top_node in top_level_nodes:
            _flattened_nodes.extend(_flatten(top_node, self.nodes))

        return _flattened_nodes

    @cached_property
    def entry_node(self) -> "DocumentNode":
        return next(
            (node for node in self.nodes if node.parent is None and node.order == 1),
            None,
        )

    def __repr__(self) -> str:
        return f"<DocumentTranslation(locale={self.locale.value};slug={self.slug})>"


class DocumentNode(Base):
    __tablename__ = "document_nodes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    nav_title: Mapped[str] = mapped_column(String, nullable=True)
    heading: Mapped[str] = mapped_column(String, nullable=True)
    subheading: Mapped[str] = mapped_column(String, nullable=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    file_content: Mapped[str] = mapped_column(Text, nullable=False)
    html_content: Mapped[str] = mapped_column(Text, nullable=False)
    document_translation_id: Mapped[int] = mapped_column(
        ForeignKey("document_translations.id"), nullable=False
    )
    parent_id: Mapped[int] = mapped_column(
        ForeignKey("document_nodes.id"), nullable=True
    )

    document_translation: Mapped[DocumentTranslation] = relationship(
        back_populates="nodes"
    )
    parent: Mapped["DocumentNode"] = relationship(
        "DocumentNode",
        back_populates="children",
        remote_side=[id],
        lazy="joined",
    )
    children: Mapped[list["DocumentNode"]] = relationship(
        "DocumentNode", back_populates="parent", order_by=order, join_depth=1
    )

    __table_args__ = (UniqueConstraint("slug", "document_translation_id"),)

    @property
    def root_parent(self):
        return self.document_translation.entry_node

    @property
    def next(self):
        nodes = self.document_translation.flattened_nodes
        current_index = nodes.index(self)
        if current_index < len(nodes) - 1:
            return nodes[current_index + 1]
        return None

    @property
    def previous(self):
        nodes = self.document_translation.flattened_nodes
        current_index = nodes.index(self)
        if current_index > 0:
            return nodes[current_index - 1]
        return None
