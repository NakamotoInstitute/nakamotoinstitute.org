from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sni.constants import LocaleType
from sni.models import DocumentTranslation


async def get(
    slug: str, *, db_session: AsyncSession, locale: LocaleType
) -> DocumentTranslation:
    return await db_session.scalar(
        select(DocumentTranslation).filter_by(slug=slug, locale=locale)
    )


async def get_all(*, db_session: AsyncSession) -> List[DocumentTranslation]:
    return (await db_session.scalars(select(DocumentTranslation))).all()


async def get_all_by_locale(
    *, db_session: AsyncSession, locale: LocaleType
) -> List[DocumentTranslation]:
    return (
        await db_session.scalars(
            select(DocumentTranslation)
            .filter(DocumentTranslation.locale == locale)
            .order_by(DocumentTranslation.sort_title.asc())
        )
    ).all()
