from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from sni.constants import LocaleType
from sni.models import Document, DocumentTranslation


async def get(
    slug: str, *, db_session: AsyncSession, locale: LocaleType
) -> DocumentTranslation:
    query = (
        select(DocumentTranslation)
        .options(
            joinedload(DocumentTranslation.document).options(
                selectinload(Document.authors),
                selectinload(Document.translations),
            ),
            selectinload(DocumentTranslation.formats),
            selectinload(DocumentTranslation.translators),
        )
        .filter_by(slug=slug, locale=locale)
    )
    return await db_session.scalar(query)


async def get_params(*, db_session: AsyncSession) -> List[DocumentTranslation]:
    query = select(DocumentTranslation.slug, DocumentTranslation.locale)

    result = await db_session.execute(query)
    all_params = result.all()

    return [dict(slug=slug, locale=locale) for (slug, locale) in all_params]


async def get_all_by_locale(
    *, db_session: AsyncSession, locale: LocaleType
) -> List[DocumentTranslation]:
    query = (
        select(DocumentTranslation)
        .options(
            joinedload(DocumentTranslation.document).options(
                selectinload(Document.authors),
                selectinload(Document.translations),
            ),
            selectinload(DocumentTranslation.formats),
        )
        .join(Document)
        .filter(DocumentTranslation.locale == locale)
        .order_by(Document.weight.desc(), DocumentTranslation.sort_title.asc())
    )

    result = await db_session.scalars(query)
    return result.all()
