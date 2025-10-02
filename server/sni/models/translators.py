from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sni.database import Base
from sni.models.library import document_translators
from sni.models.mempool import blog_post_translators

if TYPE_CHECKING:
    from sni.models.content import HTMLRenderableContent
    from sni.models.library import DocumentTranslation
    from sni.models.mempool import BlogPostTranslation


class Translator(Base):
    __tablename__ = "translators"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content_id: Mapped[int] = mapped_column(ForeignKey("content.id"), unique=True)
    content: Mapped["HTMLRenderableContent"] = relationship(uselist=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=True)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    posts: Mapped[list["BlogPostTranslation"]] = relationship(
        secondary=blog_post_translators, back_populates="translators"
    )
    docs: Mapped[list["DocumentTranslation"]] = relationship(
        secondary=document_translators, back_populates="translators"
    )

    def __repr__(self):
        return f"<Translator {self.name}>"
