from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from sni.config import LocaleType
from sni.models import DocumentTranslation


def get(slug: str, *, db_session: Session, locale: LocaleType) -> DocumentTranslation:
    return db_session.scalar(
        select(DocumentTranslation).filter_by(slug=slug, locale=locale)
    )


def get_all(*, db_session: Session) -> List[DocumentTranslation]:
    return db_session.scalars(select(DocumentTranslation)).all()


def get_all_by_locale(
    *, db_session: Session, locale: LocaleType
) -> List[DocumentTranslation]:
    return db_session.scalars(
        select(DocumentTranslation)
        .filter(DocumentTranslation.locale == locale)
        .order_by(DocumentTranslation.sort_title.asc())
    ).all()
