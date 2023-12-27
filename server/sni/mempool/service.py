from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from sni.config import LocaleType
from sni.models import BlogPost, BlogPostTranslation, BlogSeries, BlogSeriesTranslation


def get_post(
    slug: str, *, db_session: Session, locale: LocaleType = "en"
) -> BlogPostTranslation:
    return db_session.scalar(
        select(BlogPostTranslation).filter_by(slug=slug, locale=locale)
    )


def get_all_posts(*, db_session: Session) -> List[BlogPostTranslation]:
    return db_session.scalars(select(BlogPostTranslation)).all()


def get_all_posts_by_locale(
    *, db_session: Session, locale: LocaleType = "en"
) -> List[BlogPostTranslation]:
    return db_session.scalars(
        select(BlogPostTranslation)
        .join(BlogPost)
        .filter(BlogPostTranslation.locale == locale)
        .order_by(BlogPost.added.desc())
    ).all()


def get_latest_post(
    *, db_session: Session, locale: LocaleType = "en"
) -> BlogPostTranslation:
    return db_session.scalar(
        select(BlogPostTranslation)
        .filter_by(locale=locale)
        .join(BlogPost)
        .order_by(BlogPost.added.desc())
    )


def get_series(
    slug: str, *, db_session: Session, locale: LocaleType = "en"
) -> BlogSeriesTranslation:
    return db_session.scalar(
        select(BlogSeriesTranslation).filter_by(slug=slug, locale=locale)
    )


def get_series_posts(
    series: BlogSeriesTranslation, *, db_session: Session, locale: LocaleType = "en"
) -> List[BlogPostTranslation]:
    return db_session.scalars(
        select(BlogPostTranslation)
        .join(BlogPost)
        .join(BlogSeries)
        .filter(
            BlogPostTranslation.locale == locale, BlogSeries.id == series.blog_series.id
        )
    ).all()


def get_all_series(*, db_session: Session) -> List[BlogSeriesTranslation]:
    return db_session.scalars(select(BlogSeriesTranslation)).all()


def get_all_series_by_locale(
    *, db_session: Session, locale: LocaleType = "en"
) -> List[BlogSeriesTranslation]:
    return db_session.scalars(
        select(BlogSeriesTranslation)
        .join(BlogSeries)
        .filter(BlogSeriesTranslation.locale == locale)
    ).all()
