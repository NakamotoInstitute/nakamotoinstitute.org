from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from sni.config import LocaleType
from sni.database import get_db
from sni.shared.feed import FeedFormat
from sni.shared.responses import AtomResponse, RSSResponse
from sni.shared.schemas import SlugParamModel

from .feed import generate_mempool_feed
from .schemas import (
    MempoolPostIndexModel,
    MempoolPostModel,
    MempoolSeriesFullModel,
    MempoolSeriesModel,
)
from .service import (
    get_all_posts,
    get_all_posts_by_locale,
    get_all_series,
    get_all_series_by_locale,
    get_latest_post,
    get_post,
    get_series,
    get_series_posts,
)

series_router = APIRouter()


@series_router.get("", response_model=List[MempoolSeriesModel])
async def get_all_mempool_series(
    locale: LocaleType = "en", db: AsyncSession = Depends(get_db)
):
    return await get_all_series_by_locale(db_session=db, locale=locale)


@series_router.get("/params", response_model=List[SlugParamModel])
async def get_mempool_series_params(db: AsyncSession = Depends(get_db)):
    all_series = await get_all_series(db_session=db)
    return [{"locale": series.locale, "slug": series.slug} for series in all_series]


@series_router.get("/{slug}", response_model=MempoolSeriesFullModel)
async def get_mempool_series(
    slug: str, locale: LocaleType = "en", db: AsyncSession = Depends(get_db)
):
    series = await get_series(slug, db_session=db, locale=locale)
    if not series:
        raise HTTPException(status_code=404, detail="Mempool series not found")

    posts = await get_series_posts(series, db_session=db, locale=locale)

    return {"series": series, "posts": posts}


router = APIRouter()
router.include_router(series_router, prefix="/series")


@router.get("", response_model=List[MempoolPostIndexModel])
async def get_mempool_posts(
    locale: LocaleType = "en", db: AsyncSession = Depends(get_db)
):
    return await get_all_posts_by_locale(db_session=db, locale=locale)


@router.get("/latest", response_model=MempoolPostIndexModel)
async def get_latest_mempool_post(
    locale: LocaleType = "en", db: AsyncSession = Depends(get_db)
):
    post = await get_latest_post(db_session=db, locale=locale)
    if not post:
        raise HTTPException(status_code=404, detail="Mempool post not found")

    return post


@router.get("/params", response_model=List[SlugParamModel])
async def get_mempool_params(db: AsyncSession = Depends(get_db)):
    posts = await get_all_posts(db_session=db)
    return [{"locale": post.locale, "slug": post.slug} for post in posts]


@router.get("/feed", response_class=Response)
async def generate_feed(
    locale: LocaleType = "en",
    format: FeedFormat = FeedFormat.rss,
    db: Session = Depends(get_db),
):
    posts = await get_all_posts_by_locale(db_session=db, locale=locale)
    feed = generate_mempool_feed(posts, locale, format)

    if format == FeedFormat.rss:
        return RSSResponse(content=feed.rss_str(pretty=True))
    else:
        return AtomResponse(content=feed.atom_str(pretty=True))


@router.get("/{slug}", response_model=MempoolPostModel)
async def get_mempool_post(
    slug: str, locale: LocaleType = "en", db: AsyncSession = Depends(get_db)
):
    post = await get_post(slug, db_session=db, locale=locale)
    if not post:
        raise HTTPException(status_code=404, detail="Mempool post not found")

    return post
