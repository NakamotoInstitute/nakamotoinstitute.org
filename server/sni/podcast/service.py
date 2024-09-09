from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from sni.models import Episode


async def get(slug: str, *, db_session: AsyncSession) -> Episode | None:
    query = select(Episode).options(selectinload(Episode.content)).filter_by(slug=slug)

    return await db_session.scalar(query)


async def get_all(*, db_session: AsyncSession) -> Sequence[Episode]:
    query = (
        select(Episode)
        .options(selectinload(Episode.content))
        .order_by(Episode.date.desc())
    )

    result = await db_session.scalars(query)
    return result.all()
