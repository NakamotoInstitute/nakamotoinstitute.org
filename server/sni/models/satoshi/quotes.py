import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sni.database import Base
from sni.models.content import JSONContent

if TYPE_CHECKING:
    from sni.models.satoshi.emails import Email
    from sni.models.satoshi.posts import ForumPost


quote_quote_categories = Table(
    "quote_quote_categories",
    Base.metadata,
    Column("quote_id", Integer, ForeignKey("quotes.id", ondelete="CASCADE")),
    Column(
        "quote_category_id",
        Integer,
        ForeignKey("quote_categories.id", ondelete="CASCADE"),
    ),
)


class QuoteCategory(Base):
    __tablename__ = "quote_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    quotes: Mapped[List["Quote"]] = relationship(
        secondary=quote_quote_categories, back_populates="categories"
    )
    content_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("json_content.id", ondelete="CASCADE"), nullable=False
    )
    content: Mapped[JSONContent] = relationship("JSONContent")

    def __repr__(self) -> str:
        return f"<QuoteCategory({self.slug})"


class Quote(Base):
    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    whitepaper: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    email_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("emails.satoshi_id", ondelete="CASCADE"), nullable=True
    )
    email: Mapped["Email"] = relationship(back_populates="quotes")
    post_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("forum_posts.satoshi_id", ondelete="CASCADE"), nullable=True
    )
    post: Mapped["ForumPost"] = relationship(back_populates="quotes")
    categories: Mapped[List[QuoteCategory]] = relationship(
        secondary=quote_quote_categories, back_populates="quotes"
    )
    content_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("json_content.id", ondelete="CASCADE"), nullable=False
    )
    content: Mapped[JSONContent] = relationship("JSONContent")
