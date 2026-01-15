from typing import Any

from fastapi import APIRouter, HTTPException, Response, status
from pydantic.types import PositiveInt

from sni.shared.dependencies import DB, Locale
from sni.shared.feed import FeedFormat
from sni.shared.responses import AtomResponse, RSSResponse
from sni.shared.schemas import ErrorModel, SlugParamModel

from . import service
from .feed import generate_mempool_feed
from .schemas import (
    MempoolPostIndexModel,
    MempoolPostModel,
    MempoolSeriesFullModel,
    MempoolSeriesModel,
)

series_router = APIRouter()


@series_router.get(
    "",
    summary="Get all series",
    response_model=list[MempoolSeriesModel],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "All series"}},
)
async def get_all_mempool_series(locale: Locale, db: DB) -> Any:
    return await service.get_all_series_by_locale(db_session=db, locale=locale)


@series_router.get(
    "/params",
    summary="Get series params",
    response_model=list[SlugParamModel],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "Series slugs for SSG"}},
)
async def get_mempool_series_params(db: DB) -> Any:
    """Get series slugs for static site generation."""
    return await service.get_series_params(db_session=db)


@series_router.get(
    "/{slug}",
    summary="Get series by slug",
    response_model=MempoolSeriesFullModel,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Series with posts"},
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorModel,
            "description": "Mempool series not found",
        },
    },
)
async def get_mempool_series(slug: str, locale: Locale, db: DB) -> Any:
    """Returns series details with all posts in the series."""
    series = await service.get_series(slug, db_session=db, locale=locale)
    if not series:
        raise HTTPException(status_code=404, detail="Mempool series not found")

    posts = await service.get_series_posts(
        series.blog_series.id, db_session=db, locale=locale
    )

    return {"series": series, "posts": posts}


router = APIRouter()
router.include_router(series_router, prefix="/series")


@router.get(
    "",
    summary="Get all posts",
    response_model=list[MempoolPostIndexModel],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "All posts"}},
)
async def get_mempool_posts(locale: Locale, db: DB) -> Any:
    return await service.get_all_posts_by_locale(db_session=db, locale=locale)


@router.get(
    "/latest",
    summary="Get latest posts",
    response_model=list[MempoolPostIndexModel],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "Latest N posts"}},
)
async def get_latest_mempool_posts(locale: Locale, db: DB, num: PositiveInt = 3) -> Any:
    """Returns the N most recent posts. Defaults to 3."""
    return await service.get_latest_posts(db_session=db, locale=locale, num=num)


@router.get(
    "/params",
    summary="Get post params",
    response_model=list[SlugParamModel],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "Post slugs for SSG"}},
)
async def get_mempool_params(db: DB) -> Any:
    """Get post slugs for static site generation."""
    return await service.get_params(db_session=db)


@router.get(
    "/feed",
    summary="Get RSS/Atom feed",
    response_class=Response,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "RSS/Atom feed"}},
)
async def generate_feed(
    locale: Locale, db: DB, format: FeedFormat = FeedFormat.rss
) -> Any:
    """Returns RSS or Atom feed based on format parameter."""
    posts = await service.get_all_posts_by_locale(db_session=db, locale=locale)
    feed = generate_mempool_feed(posts, locale, format)

    if format == FeedFormat.rss:
        return RSSResponse(content=feed.rss_str(pretty=True))
    else:
        return AtomResponse(content=feed.atom_str(pretty=True))


@router.get(
    "/{slug}",
    summary="Get post by slug",
    response_model=MempoolPostModel,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Post with content"},
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorModel,
            "description": "Mempool post not found",
        },
    },
)
async def get_mempool_post(slug: str, locale: Locale, db: DB) -> Any:
    post = await service.get_post(slug, db_session=db, locale=locale)
    if not post:
        raise HTTPException(status_code=404, detail="Mempool post not found")

    return post
