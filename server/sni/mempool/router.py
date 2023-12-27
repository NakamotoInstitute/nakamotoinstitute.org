from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from sni.config import LocaleType
from sni.database import get_db
from sni.shared.schemas import SlugParamModel

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
def get_all_mempool_series(locale: LocaleType = "en", db: Session = Depends(get_db)):
    return get_all_series_by_locale(db_session=db, locale=locale)


@series_router.get("/params", response_model=List[SlugParamModel])
def get_mempool_series_params(db: Session = Depends(get_db)):
    all_series = get_all_series(db_session=db)
    return [{"locale": series.locale, "slug": series.slug} for series in all_series]


@series_router.get("/{slug}", response_model=MempoolSeriesFullModel)
def get_mempool_series(
    slug: str, locale: LocaleType = "en", db: Session = Depends(get_db)
):
    series = get_series(slug, db_session=db, locale=locale)
    if not series:
        raise HTTPException(status_code=404, detail="Mempool series not found")

    posts = get_series_posts(series, db_session=db, locale=locale)

    return {"series": series, "posts": posts}


router = APIRouter()
router.include_router(series_router, prefix="/series")


@router.get("", response_model=List[MempoolPostIndexModel])
def get_mempool_posts(locale: LocaleType = "en", db: Session = Depends(get_db)):
    return get_all_posts_by_locale(db_session=db, locale=locale)


@router.get("/latest", response_model=MempoolPostModel)
def get_latest_mempool_post(locale: LocaleType = "en", db: Session = Depends(get_db)):
    post = get_latest_post(db_session=db, locale=locale)
    if not post:
        raise HTTPException(status_code=404, detail="Mempool post not found")

    return post


@router.get("/params", response_model=List[SlugParamModel])
def get_mempool_params(db: Session = Depends(get_db)):
    posts = get_all_posts(db_session=db)
    return [{"locale": post.locale, "slug": post.slug} for post in posts]


@router.get("/{slug}", response_model=MempoolPostModel)
def get_mempool_post(
    slug: str, locale: LocaleType = "en", db: Session = Depends(get_db)
):
    post = get_post(slug, db_session=db, locale=locale)
    if not post:
        raise HTTPException(status_code=404, detail="Mempool post not found")

    return post
