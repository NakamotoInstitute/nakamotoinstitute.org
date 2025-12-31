from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from sni.models import Email, ForumPost, Quote, QuoteCategory


async def get_category(slug: str, *, db_session: AsyncSession) -> QuoteCategory | None:
    query = select(QuoteCategory).filter_by(slug=slug)

    return await db_session.scalar(query)


async def get_category_quotes(
    slug: str, *, db_session: AsyncSession
) -> Sequence[Quote]:
    query = (
        select(Quote)
        .options(
            joinedload(Quote.email).joinedload(Email.thread),
            joinedload(Quote.post).joinedload(ForumPost.thread),
            selectinload(Quote.categories),
        )
        .join(QuoteCategory, Quote.categories)
        .filter(QuoteCategory.slug == slug)
        .order_by(Quote.date)
    )

    result = await db_session.scalars(query)
    return result.all()


async def get_all(*, db_session: AsyncSession) -> Sequence[QuoteCategory]:
    query = select(QuoteCategory).order_by(QuoteCategory.slug)

    result = await db_session.scalars(query)
    return result.all()
