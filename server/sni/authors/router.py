from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sni.config import LocaleType
from sni.database import get_db
from sni.shared.schemas import SlugParamModel

from .schemas.response import AuthorDetailModel, AuthorModel
from .service import (
    check_blog_posts_exist,
    check_documents_exist,
    get,
    get_all,
    get_all_author_locales,
    get_all_by_locale,
    get_author_locales,
    get_blog_posts,
    get_documents,
)

router = APIRouter()


@router.get("", response_model=List[AuthorModel])
async def get_authors(locale: LocaleType = "en", db: AsyncSession = Depends(get_db)):
    return await get_all_by_locale(db_session=db, locale=locale)


@router.get("/params", response_model=List[SlugParamModel])
async def get_author_params(db: AsyncSession = Depends(get_db)):
    valid_combinations = []

    authors = await get_all(db_session=db)
    locales = await get_all_author_locales(db_session=db)

    for author in authors:
        for locale in locales:
            mempool_posts_exist = await check_blog_posts_exist(
                author, db_session=db, locale=locale
            )
            library_docs_exist = await check_documents_exist(
                author, db_session=db, locale=locale
            )

            if mempool_posts_exist or library_docs_exist:
                valid_combinations.append({"slug": author.slug, "locale": locale})

    return valid_combinations


@router.get("/{slug}", response_model=AuthorDetailModel)
async def get_author(
    slug: str, locale: LocaleType = "en", db: AsyncSession = Depends(get_db)
):
    author = await get(slug, db_session=db)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    locales = await get_author_locales(author, db_session=db)

    mempool_posts = await get_blog_posts(author, db_session=db, locale=locale)
    library_docs = await get_documents(author, db_session=db, locale=locale)

    if not mempool_posts and not library_docs:
        raise HTTPException(status_code=404, detail="Author not found")

    return {
        "author": author,
        "library": library_docs,
        "mempool": mempool_posts,
        "locales": locales,
    }
