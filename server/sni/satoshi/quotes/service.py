from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from sni.models import Email, ForumPost, Quote, QuoteCategory


async def get(slug: str, *, db_session: AsyncSession) -> QuoteCategory:
    query = (
        select(QuoteCategory)
        .options(
            selectinload(QuoteCategory.quotes).options(
                joinedload(Quote.email).joinedload(Email.thread),
                joinedload(Quote.post).joinedload(ForumPost.thread),
                selectinload(Quote.categories),
            )
        )
        .filter_by(slug=slug)
    )

    return await db_session.scalar(query)


async def get_all(*, db_session: AsyncSession) -> List[QuoteCategory]:
    query = select(QuoteCategory).order_by(QuoteCategory.slug)

    result = await db_session.scalars(query)
    return result
