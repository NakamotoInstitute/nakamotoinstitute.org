import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, Date, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sni.extensions import db

if TYPE_CHECKING:
    from sni.satoshi.emails.models import Email
    from sni.satoshi.posts.models import ForumPost


quote_quote_categories = db.Table(
    "quote_quote_categories",
    db.Column("quote_id", db.Integer, db.ForeignKey("quotes.id")),
    db.Column("quote_category_id", db.Integer, db.ForeignKey("quote_categories.id")),
)


class QuoteCategory(db.Model):
    __tablename__ = "quote_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    quotes: Mapped[List["Quote"]] = relationship(
        secondary=quote_quote_categories, back_populates="categories"
    )

    def __repr__(self) -> str:
        return f"<QuoteCategory({self.slug})"


class Quote(db.Model):
    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    whitepaper: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    email_id: Mapped[int] = mapped_column(
        Integer, db.ForeignKey("emails.satoshi_id"), nullable=True
    )
    email: Mapped["Email"] = relationship(back_populates="quotes")
    post_id: Mapped[int] = mapped_column(
        Integer, db.ForeignKey("forum_posts.satoshi_id"), nullable=True
    )
    post: Mapped["ForumPost"] = relationship(back_populates="quotes")
    categories: Mapped[List[QuoteCategory]] = relationship(
        secondary=quote_quote_categories, back_populates="quotes"
    )
