from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sni.models import QuoteCategory


async def get(slug: str, *, db_session: AsyncSession) -> QuoteCategory:
    return await db_session.scalar(select(QuoteCategory).filter_by(slug=slug))


async def get_all(*, db_session: AsyncSession) -> List[QuoteCategory]:
    return (
        await db_session.scalars(select(QuoteCategory).order_by(QuoteCategory.slug))
    ).all()
