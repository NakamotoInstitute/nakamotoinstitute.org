from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from sni.models import Email, EmailThread


def get_all_emails(*, db_session: Session) -> List[Email]:
    return db_session.scalars(
        select(Email).filter(Email.satoshi_id.isnot(None)).order_by(Email.date)
    ).all()


def get_threads(*, db_session: Session) -> List[EmailThread]:
    return db_session.scalars(select(EmailThread)).all()


def get_satoshi_emails_by_source(source: str, *, db_session: Session) -> List[Email]:
    return db_session.scalars(
        select(Email)
        .filter(Email.satoshi_id.isnot(None))
        .join(EmailThread)
        .filter_by(source=source)
        .order_by(Email.date)
    ).all()


def get_satoshi_email_by_source(
    source: str, satoshi_id: int, *, db_session: Session
) -> Email:
    return db_session.scalar(
        select(Email)
        .filter_by(satoshi_id=satoshi_id)
        .join(EmailThread)
        .filter_by(source=source)
    )


def get_email(satoshi_id: int, *, db_session: Session) -> Email:
    return db_session.scalar(select(Email).filter_by(satoshi_id=satoshi_id))


def get_threads_by_source(source: str, *, db_session: Session) -> List[EmailThread]:
    return db_session.scalars(
        select(EmailThread).filter_by(source=source).order_by(EmailThread.id)
    ).all()


def get_thread_emails(
    source: str, thread_id: int, satoshi: bool, *, db_session: Session
) -> List[Email]:
    emails_query = (
        select(Email)
        .join(EmailThread)
        .filter(Email.thread_id == thread_id, EmailThread.source == source)
    )
    if satoshi:
        emails_query = emails_query.filter(Email.satoshi_id.isnot(None))

    return db_session.scalars(emails_query).all()


def get_thread(thread_id: int, *, db_session: Session) -> EmailThread:
    return db_session.scalar(select(EmailThread).filter_by(id=thread_id))
