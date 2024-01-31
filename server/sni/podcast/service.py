from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sni.models import Episode


async def get(slug: str, *, db_session: AsyncSession) -> Episode:
    return await db_session.scalar(select(Episode).filter_by(slug=slug))


async def get_all(*, db_session: AsyncSession) -> List[Episode]:
    return (
        await db_session.scalars(select(Episode).order_by(Episode.date.desc()))
    ).all()
