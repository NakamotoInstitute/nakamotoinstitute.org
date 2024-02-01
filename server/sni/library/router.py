from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sni.constants import LocaleType
from sni.database import get_db
from sni.shared.schemas import SlugParamModel

from .schemas import DocumentIndexModel, DocumentModel
from .service import get, get_all, get_all_by_locale

router = APIRouter()


@router.get("", response_model=List[DocumentIndexModel])
async def get_library_docs(
    locale: LocaleType = "en", db: AsyncSession = Depends(get_db)
):
    return await get_all_by_locale(db_session=db, locale=locale)


@router.get("/params", response_model=List[SlugParamModel])
async def get_library_params(db: AsyncSession = Depends(get_db)):
    docs = await get_all(db_session=db)
    return [{"locale": doc.locale, "slug": doc.slug} for doc in docs]


@router.get("/{slug}", response_model=DocumentModel)
async def get_library_doc(
    slug: str, locale: LocaleType = "en", db: AsyncSession = Depends(get_db)
):
    doc = await get(slug, db_session=db, locale=locale)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    return doc
