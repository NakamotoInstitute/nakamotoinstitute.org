from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from sni.constants import LocaleType
from sni.models import BlogPost, BlogPostTranslation, BlogSeries, BlogSeriesTranslation


async def get_post(
    slug: str, *, db_session: AsyncSession, locale: LocaleType = "en"
) -> BlogPostTranslation:
    return await db_session.scalar(
        select(BlogPostTranslation).filter_by(slug=slug, locale=locale)
    )


async def get_all_posts(*, db_session: AsyncSession) -> List[BlogPostTranslation]:
    return (await db_session.scalars(select(BlogPostTranslation))).all()


async def get_all_posts_by_locale(
    *, db_session: Session, locale: LocaleType = "en"
) -> List[BlogPostTranslation]:
    return (
        await db_session.scalars(
            select(BlogPostTranslation)
            .join(BlogPost)
            .filter(BlogPostTranslation.locale == locale)
            .order_by(BlogPost.added.desc())
        )
    ).all()


async def get_latest_post(
    *, db_session: AsyncSession, locale: LocaleType = "en"
) -> BlogPostTranslation:
    return await db_session.scalar(
        select(BlogPostTranslation)
        .filter_by(locale=locale)
        .join(BlogPost)
        .order_by(BlogPost.added.desc())
    )


async def get_series(
    slug: str, *, db_session: AsyncSession, locale: LocaleType = "en"
) -> BlogSeriesTranslation:
    return await db_session.scalar(
        select(BlogSeriesTranslation).filter_by(slug=slug, locale=locale)
    )


async def get_series_posts(
    series: BlogSeriesTranslation,
    *,
    db_session: AsyncSession,
    locale: LocaleType = "en"
) -> List[BlogPostTranslation]:
    return (
        await db_session.scalars(
            select(BlogPostTranslation)
            .join(BlogPost)
            .join(BlogSeries)
            .filter(
                BlogPostTranslation.locale == locale,
                BlogSeries.id == series.blog_series.id,
            )
        )
    ).all()


async def get_all_series(*, db_session: AsyncSession) -> List[BlogSeriesTranslation]:
    return (await db_session.scalars(select(BlogSeriesTranslation))).all()


async def get_all_series_by_locale(
    *, db_session: AsyncSession, locale: LocaleType = "en"
) -> List[BlogSeriesTranslation]:
    return (
        await db_session.scalars(
            select(BlogSeriesTranslation)
            .join(BlogSeries)
            .filter(BlogSeriesTranslation.locale == locale)
        )
    ).all()
