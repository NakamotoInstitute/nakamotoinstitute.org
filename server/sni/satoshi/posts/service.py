from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from sni.models import ForumPost, ForumThread


def get_all_posts(*, db_session: Session) -> List[ForumPost]:
    return db_session.scalars(
        select(ForumPost)
        .filter(ForumPost.satoshi_id.isnot(None))
        .order_by(ForumPost.date)
    ).all()


def get_threads(*, db_session: Session) -> List[ForumThread]:
    return db_session.scalars(select(ForumThread)).all()


def get_posts_by_source(source: str, *, db_session: Session) -> List[ForumPost]:
    return db_session.scalars(
        select(ForumPost)
        .filter(ForumPost.satoshi_id.isnot(None))
        .join(ForumThread)
        .filter_by(source=source)
        .order_by(ForumPost.date)
    ).all()


def get_post_by_source(
    source: str, satoshi_id: int, *, db_session: Session
) -> ForumPost:
    return db_session.scalar(
        select(ForumPost)
        .filter_by(satoshi_id=satoshi_id)
        .join(ForumThread)
        .filter_by(source=source)
    )


def get_post(satoshi_id: int, *, db_session: Session) -> ForumPost:
    return db_session.scalar(select(ForumPost).filter_by(satoshi_id=satoshi_id))


def get_threads_by_source(source: str, *, db_session: Session) -> List[ForumThread]:
    return db_session.scalars(
        select(ForumThread).filter_by(source=source).order_by(ForumThread.id)
    ).all()


def get_thread_posts(
    source: str, thread_id: int, satoshi: bool, *, db_session: Session
) -> List[ForumPost]:
    posts_query = (
        select(ForumPost)
        .join(ForumThread)
        .filter(ForumPost.thread_id == thread_id, ForumThread.source == source)
    )
    if satoshi:
        posts_query = posts_query.filter(ForumPost.satoshi_id.isnot(None))

    return db_session.scalars(posts_query).all()


def get_thread(thread_id: int, *, db_session: Session) -> ForumThread:
    return db_session.scalar(select(ForumThread).filter_by(id=thread_id))
