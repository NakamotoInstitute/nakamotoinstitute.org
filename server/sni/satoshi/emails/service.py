from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from sni.models import Email, EmailThread


async def get_all_emails(*, db_session: AsyncSession) -> List[Email]:
    query = (
        select(Email)
        .options(joinedload(Email.thread), selectinload(Email.replies))
        .filter(Email.satoshi_id.isnot(None))
        .order_by(Email.date)
    )

    result = await db_session.scalars(query)
    return result.all()


async def get_threads(*, db_session: AsyncSession) -> List[EmailThread]:
    query = select(EmailThread).options(selectinload(EmailThread.emails))

    result = await db_session.scalars(query)
    return result.all()


async def get_satoshi_emails_by_source(
    source: str, *, db_session: AsyncSession
) -> List[Email]:
    query = (
        select(Email)
        .options(joinedload(Email.thread), selectinload(Email.replies))
        .filter(Email.satoshi_id.isnot(None))
        .join(EmailThread)
        .filter_by(source=source)
        .order_by(Email.date)
    )

    result = await db_session.scalars(query)
    return result.all()


async def get_satoshi_email_by_source(
    source: str, satoshi_id: int, *, db_session: AsyncSession
) -> Email:
    query = (
        select(Email)
        .options(joinedload(Email.thread), selectinload(Email.replies))
        .filter_by(satoshi_id=satoshi_id)
        .join(EmailThread)
        .filter_by(source=source)
    )

    return await db_session.scalar(query)


async def get_email(satoshi_id: int, *, db_session: AsyncSession) -> Email:
    query = (
        select(Email)
        .options(selectinload(Email.replies))
        .filter_by(satoshi_id=satoshi_id)
    )

    return await db_session.scalar(query)


async def get_threads_by_source(
    source: str, *, db_session: AsyncSession
) -> List[EmailThread]:
    query = (
        select(EmailThread)
        .options(selectinload(EmailThread.emails))
        .filter_by(source=source)
        .order_by(EmailThread.id)
    )

    result = await db_session.scalars(query)
    return result.all()


async def get_thread(
    thread_id: int, *, db_session: AsyncSession, emails: bool = False
) -> EmailThread:
    email_loader_options = []
    if emails:
        email_loader_options = [
            joinedload(Email.parent).selectinload(Email.replies),
            selectinload(Email.replies),
        ]

    query = (
        select(EmailThread)
        .options(selectinload(EmailThread.emails).options(*email_loader_options))
        .filter_by(id=thread_id)
    )

    return await db_session.scalar(query)
