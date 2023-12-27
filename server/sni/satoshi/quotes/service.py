from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from sni.models import QuoteCategory


def get(slug: str, *, db_session: Session) -> QuoteCategory:
    return db_session.scalar(select(QuoteCategory).filter_by(slug=slug))


def get_all(*, db_session: Session) -> List[QuoteCategory]:
    return db_session.scalars(select(QuoteCategory).order_by(QuoteCategory.slug)).all()
