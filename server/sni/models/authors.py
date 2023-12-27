from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sni.models.content import MarkdownContent
from sni.models.library import document_authors
from sni.models.mempool import blog_post_authors

if TYPE_CHECKING:
    from sni.models.library import Document
    from sni.models.mempool import BlogPost


class Author(MarkdownContent):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(
        Integer, ForeignKey("markdown_content.id"), primary_key=True
    )
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    sort_name: Mapped[str] = mapped_column(String, nullable=False)
    posts: Mapped[List["BlogPost"]] = relationship(
        secondary=blog_post_authors, back_populates="authors"
    )
    docs: Mapped[List["Document"]] = relationship(
        secondary=document_authors, back_populates="authors"
    )

    __mapper_args__ = {"polymorphic_identity": "author"}

    def __repr__(self) -> str:
        return f"<Author({self.slug})>"
