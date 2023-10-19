from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sni.extensions import db
from sni.library.models import document_translators
from sni.mempool.models import blog_post_translators

if TYPE_CHECKING:
    from sni.library.models import DocumentTranslation
    from sni.mempool.models import BlogPostTranslation


class Translator(db.Model):
    __tablename__ = "translators"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=True)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posts: Mapped[List["BlogPostTranslation"]] = relationship(
        secondary=blog_post_translators, back_populates="translators"
    )
    docs: Mapped[List["DocumentTranslation"]] = relationship(
        secondary=document_translators, back_populates="translators"
    )

    def __repr__(self):
        return f"<Translator {self.name}>"
