from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sni.models.content import MarkdownContent
from sni.models.library import document_translators
from sni.models.mempool import blog_post_translators

if TYPE_CHECKING:
    from sni.models.library import DocumentTranslation
    from sni.models.mempool import BlogPostTranslation


class Translator(MarkdownContent):
    __tablename__ = "translators"

    id: Mapped[int] = mapped_column(
        Integer, ForeignKey("markdown_content.id"), primary_key=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=True)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    posts: Mapped[List["BlogPostTranslation"]] = relationship(
        secondary=blog_post_translators, back_populates="translators", lazy="selectin"
    )
    docs: Mapped[List["DocumentTranslation"]] = relationship(
        secondary=document_translators, back_populates="translators", lazy="selectin"
    )

    __mapper_args__ = {"polymorphic_identity": "translator"}

    def __repr__(self):
        return f"<Translator {self.name}>"
