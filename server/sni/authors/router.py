from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sni.constants import LocaleType
from sni.database import get_db
from sni.shared.schemas import SlugParamModel

from . import service
from .schemas.response import AuthorDetailModel, AuthorModel

router = APIRouter()


@router.get("")
async def get_authors(
    locale: LocaleType = "en", db: AsyncSession = Depends(get_db)
) -> List[AuthorModel]:
    return await service.get_all_by_locale(db_session=db, locale=locale)


@router.get("/params", response_model=List[SlugParamModel])
async def get_author_params(db: AsyncSession = Depends(get_db)):
    return await service.get_params(db_session=db)


@router.get("/{slug}", response_model=AuthorDetailModel)
async def get_author(
    slug: str, locale: LocaleType = "en", db: AsyncSession = Depends(get_db)
):
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
