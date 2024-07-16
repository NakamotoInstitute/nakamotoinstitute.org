from typing import Sequence

from sqlalchemy import case, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from sni.constants import LocaleType
from sni.models import Document, DocumentNode, DocumentTranslation


async def get(
    slug: str, *, db_session: AsyncSession, locale: LocaleType
) -> DocumentTranslation | None:
    query = (
        select(DocumentTranslation)
        .options(
            joinedload(DocumentTranslation.document).options(
                selectinload(Document.authors),
                selectinload(Document.translations),
            ),
            selectinload(DocumentTranslation.formats),
            selectinload(DocumentTranslation.translators),
            selectinload(DocumentTranslation.nodes),
        )
        .filter_by(slug=slug, locale=locale)
    )
    return await db_session.scalar(query)


async def get_node(
    slug: str, *, doc_slug: str, db_session: AsyncSession, locale: LocaleType
) -> DocumentNode | None:
    query = (
        select(DocumentNode)
        .options(
            joinedload(DocumentNode.document_translation).options(
                joinedload(DocumentTranslation.document),
                selectinload(DocumentTranslation.nodes),
            )
        )
        .join(DocumentTranslation)
        .join(Document)
        .filter(
            DocumentNode.slug == slug,
            DocumentTranslation.slug == doc_slug,
            DocumentTranslation.locale == locale,
        )
    )
    return await db_session.scalar(query)


async def get_params(*, db_session: AsyncSession) -> list[dict[str, LocaleType]]:
    query = select(DocumentTranslation.slug, DocumentTranslation.locale)

    result = await db_session.execute(query)
    all_params = result.all()

    return [dict(slug=slug, locale=locale) for (slug, locale) in all_params]


async def get_all_by_locale(
    *, db_session: AsyncSession, locale: LocaleType
) -> Sequence[DocumentTranslation]:
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


async def get_some_by_slugs_and_locale(
    slugs: list[str], *, db_session: AsyncSession, locale: LocaleType
) -> Sequence[DocumentTranslation]:
    order_case = case(
        {slug: index for index, slug in enumerate(slugs)}, value=Document.slug
    )

    query = (
        select(DocumentTranslation)
        .options(
            joinedload(DocumentTranslation.document).options(
                selectinload(Document.authors),
                selectinload(Document.translations),
            ),
            selectinload(DocumentTranslation.formats),
        )
        .join(Document, DocumentTranslation.document_id == Document.id)
        .filter(DocumentTranslation.locale == locale, Document.slug.in_(slugs))
        .order_by(order_case)
    )

    result = await db_session.scalars(query)
    return result.all()
