from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from sni.models import ForumPost, ForumThread

from .schemas import ForumPostSource


async def get_all_posts(*, db_session: AsyncSession) -> Sequence[ForumPost]:
    query = (
        select(ForumPost)
        .options(joinedload(ForumPost.thread))
        .filter(ForumPost.satoshi_id.isnot(None))
        .order_by(ForumPost.date)
    )

    result = await db_session.scalars(query)
    return result.all()


async def get_threads(*, db_session: AsyncSession) -> Sequence[ForumThread]:
    query = select(ForumThread).options(selectinload(ForumThread.posts))

    result = await db_session.scalars(query)
    return result.all()


async def get_posts_by_source(
    source: str, *, db_session: AsyncSession
) -> Sequence[ForumPost]:
    query = (
        select(ForumPost)
        .options(joinedload(ForumPost.thread))
        .filter(ForumPost.satoshi_id.isnot(None))
        .join(ForumThread)
        .filter_by(source=source)
        .order_by(ForumPost.date)
    )

    result = await db_session.scalars(query)
    return result.all()


async def get_post_by_source(
    source: str, satoshi_id: int, *, db_session: AsyncSession
) -> ForumPost | None:
    query = (
        select(ForumPost)
        .options(joinedload(ForumPost.thread))
        .filter_by(satoshi_id=satoshi_id)
        .join(ForumThread)
        .filter_by(source=source)
    )

    return await db_session.scalar(query)


async def get_post(satoshi_id: int, *, db_session: AsyncSession) -> ForumPost | None:
    query = (
        select(ForumPost)
        .options(joinedload(ForumPost.thread))
        .filter_by(satoshi_id=satoshi_id)
    )

    return await db_session.scalar(query)


async def get_threads_by_source(
    source: str, *, db_session: AsyncSession
) -> Sequence[ForumThread]:
    query = (
        select(ForumThread)
        .options(selectinload(ForumThread.posts))
        .filter_by(source=source)
        .order_by(ForumThread.id)
    )

    result = await db_session.scalars(query)
    return result.all()


async def get_thread(thread_id: int, *, db_session: AsyncSession) -> ForumThread | None:
    query = select(ForumThread).filter_by(id=thread_id)

    return await db_session.scalar(query)


async def get_thread_posts(
    source: ForumPostSource, thread_id: int, satoshi: bool, *, db_session: AsyncSession
) -> Sequence[ForumPost]:
    query = (
        select(ForumPost)
        .join(ForumThread)
        .filter(ForumPost.thread_id == thread_id, ForumThread.source == source)
    )
    if satoshi:
        query = query.filter(ForumPost.satoshi_id.isnot(None))
    query = query.order_by(ForumPost.id)

    result = await db_session.scalars(query)
    return result.all()
