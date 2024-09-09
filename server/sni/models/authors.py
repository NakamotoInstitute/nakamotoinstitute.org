from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sni.database import Base
from sni.models.library import document_authors
from sni.models.mempool import blog_post_authors

if TYPE_CHECKING:
    from sni.models.content import HTMLRenderableContent
    from sni.models.library import Document
    from sni.models.mempool import BlogPost


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content_id: Mapped[int] = mapped_column(ForeignKey("content.id"), unique=True)
    content: Mapped["HTMLRenderableContent"] = relationship(uselist=False)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    sort_name: Mapped[str] = mapped_column(String, nullable=False)
    posts: Mapped[List["BlogPost"]] = relationship(
        secondary=blog_post_authors, back_populates="authors"
    )
    docs: Mapped[List["Document"]] = relationship(
        secondary=document_authors, back_populates="authors"
    )

    def __repr__(self) -> str:
        return f"<Author({self.slug})>"
