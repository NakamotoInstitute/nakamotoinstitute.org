from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from sni.constants import LocaleType
from sni.models import BlogPost, BlogPostTranslation, BlogSeries, BlogSeriesTranslation


async def get_post(
    slug: str, *, db_session: AsyncSession, locale: LocaleType = "en"
) -> BlogPostTranslation | None:
    query = (
        select(BlogPostTranslation)
        .options(
            joinedload(BlogPostTranslation.blog_post).options(
                selectinload(BlogPost.authors),
                selectinload(BlogPost.translations),
                joinedload(BlogPost.series).selectinload(BlogSeries.translations),
            ),
            selectinload(BlogPostTranslation.translators),
        )
        .filter_by(slug=slug, locale=locale)
    )
    return await db_session.scalar(query)


async def get_params(*, db_session: AsyncSession) -> list[dict[str, LocaleType]]:
    query = select(BlogPostTranslation.slug, BlogPostTranslation.locale)

    result = await db_session.execute(query)
    all_params = result.all()

    return [dict(slug=slug, locale=locale) for (slug, locale) in all_params]


async def get_all_posts_by_locale(
    *, db_session: AsyncSession, locale: LocaleType = "en"
) -> Sequence[BlogPostTranslation]:
    query = (
        select(BlogPostTranslation)
        .options(
            joinedload(BlogPostTranslation.blog_post).options(
                selectinload(BlogPost.authors),
                selectinload(BlogPost.translations),
                joinedload(BlogPost.series).selectinload(BlogSeries.translations),
            )
        )
        .join(BlogPost)
        .outerjoin(BlogSeries)
        .filter(BlogPostTranslation.locale == locale)
        .order_by(BlogPost.added.desc())
    )

    result = await db_session.scalars(query)
    return result.all()


async def get_latest_posts(
    *, db_session: AsyncSession, locale: LocaleType = "en", num: int = 3
) -> list[BlogPostTranslation]:
    num = max(1, num)

    query = (
        select(BlogPostTranslation)
        .options(
            joinedload(BlogPostTranslation.blog_post).options(
                selectinload(BlogPost.authors),
                selectinload(BlogPost.translations),
                joinedload(BlogPost.series).selectinload(BlogSeries.translations),
            )
        )
        .filter_by(locale=locale)
        .join(BlogPost)
        .order_by(BlogPost.added.desc())
        .limit(num)
    )

    result = await db_session.scalars(query)
    return result.all()


async def get_series(
    slug: str, *, db_session: AsyncSession, locale: LocaleType = "en"
) -> BlogSeriesTranslation | None:
    query = (
        select(BlogSeriesTranslation)
        .options(
            joinedload(BlogSeriesTranslation.blog_series).selectinload(
                BlogSeries.translations
            )
        )
        .filter_by(slug=slug, locale=locale)
    )

    return await db_session.scalar(query)


async def get_series_posts(
    series_id: int,
    *,
    db_session: AsyncSession,
    locale: LocaleType = "en",
) -> Sequence[BlogPostTranslation]:
    query = (
        select(BlogPostTranslation)
        .options(
            joinedload(BlogPostTranslation.blog_post).options(
                joinedload(BlogPost.series),
                selectinload(BlogPost.authors),
                selectinload(BlogPost.translations),
            )
        )
        .join(BlogPost)
        .filter(
            BlogPostTranslation.locale == locale,
            BlogPost.series_id == series_id,
        )
        .order_by(BlogPost.series_index.asc())
    )

    result = await db_session.scalars(query)
    return result.all()


async def get_series_params(*, db_session: AsyncSession) -> list[dict[str, LocaleType]]:
    query = select(BlogSeriesTranslation.slug, BlogSeriesTranslation.locale)

    result = await db_session.execute(query)
    all_params = result.all()

    return [dict(slug=slug, locale=locale) for slug, locale in all_params]


async def get_all_series_by_locale(
    *, db_session: AsyncSession, locale: LocaleType = "en"
) -> Sequence[BlogSeriesTranslation]:
    query = (
        select(BlogSeriesTranslation)
        .options(
            joinedload(BlogSeriesTranslation.blog_series).selectinload(
                BlogSeries.translations
            )
        )
        .filter(BlogSeriesTranslation.locale == locale)
    )

    result = await db_session.scalars(query)
    return result.all()
