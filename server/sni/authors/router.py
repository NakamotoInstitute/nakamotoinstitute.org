from typing import Any

from fastapi import APIRouter, HTTPException, status

from sni.shared.dependencies import DB, Locale
from sni.shared.schemas import ErrorModel, SlugParamModel

from . import service
from .schemas.response import AuthorDetailModel, AuthorModel

router = APIRouter()


@router.get(
    "",
    summary="Get all authors",
    response_model=list[AuthorModel],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "All authors"}},
)
async def get_authors(locale: Locale, db: DB) -> Any:
    return await service.get_all_by_locale(db_session=db, locale=locale)


@router.get(
    "/params",
    summary="Get author params",
    response_model=list[SlugParamModel],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "Author slugs for SSG"}},
)
async def get_author_params(db: DB) -> Any:
    """Get author slugs for static site generation."""
    return await service.get_params(db_session=db)


@router.get(
    "/{slug}",
    summary="Get author by slug",
    response_model=AuthorDetailModel,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Author with works"},
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorModel,
            "description": "Author not found",
        },
    },
)
async def get_author(slug: str, locale: Locale, db: DB) -> Any:
    """Returns author details with their library docs and mempool posts."""
    author = await service.get(slug, db_session=db, locale=locale)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    locales = await service.get_author_locales(author.id, db_session=db)

    library_docs = await service.get_documents(author.id, db_session=db, locale=locale)
    mempool_posts = await service.get_blog_posts(
        author.id, db_session=db, locale=locale
    )
    if not library_docs and not mempool_posts:
        raise HTTPException(status_code=404, detail="Author not found")

    return {
        "author": author,
        "library": library_docs,
        "mempool": mempool_posts,
        "locales": locales,
    }
