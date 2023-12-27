from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from sni.models import Episode


def get(slug: str, *, db_session: Session) -> Episode:
    return db_session.scalar(select(Episode).filter_by(slug=slug))


def get_all(*, db_session: Session) -> List[Episode]:
    return db_session.scalars(select(Episode).order_by(Episode.date.desc())).all()
