from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sni.models import Episode


async def get(slug: str, *, db_session: AsyncSession) -> Episode:
    query = select(Episode).filter_by(slug=slug)

    return await db_session.scalar(query)


async def get_all(*, db_session: AsyncSession) -> List[Episode]:
    query = select(Episode).order_by(Episode.date.desc())

    result = await db_session.scalars(query)
    return result.all()
