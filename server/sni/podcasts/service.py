from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from sni.models import Episode, Podcast


async def get_podcasts(*, db_session: AsyncSession) -> Sequence[Podcast]:
    query = select(Podcast).options(selectinload(Podcast.episodes))

    result = await db_session.scalars(query)
    return result.all()


async def get_home_podcasts(*, db_session: AsyncSession) -> Sequence[Podcast]:
    query = select(Podcast).order_by(Podcast.defunct.asc(), Podcast.sort_name)

    result = await db_session.scalars(query)
    return result.all()


async def get_podcast_by_slug(slug: str, *, db_session: AsyncSession) -> Podcast | None:
    query = (
        select(Podcast)
        .options(joinedload(Podcast.episodes).options(joinedload(Episode.content)))
        .filter_by(slug=slug)
    )

    return await db_session.scalar(query)


async def get_episodes(*, db_session: AsyncSession) -> Sequence[Episode]:
    query = select(Episode).options(
        joinedload(Episode.podcast), joinedload(Episode.content)
    )

    result = await db_session.scalars(query)
    return result.all()


async def get_episode_by_slug(slug: str, *, db_session: AsyncSession) -> Episode | None:
    query = (
        select(Episode)
        .options(joinedload(Episode.podcast), joinedload(Episode.content))
        .filter_by(slug=slug)
    )

    return await db_session.scalar(query)
