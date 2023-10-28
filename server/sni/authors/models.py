from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sni.extensions import db
from sni.library.models import document_authors
from sni.mempool.models import blog_post_authors
from sni.shared.models import MarkdownContent

if TYPE_CHECKING:
    from sni.library.models import Document
    from sni.mempool.models import BlogPost


class Author(MarkdownContent):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(
        Integer, db.ForeignKey("markdown_content.id"), primary_key=True
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
