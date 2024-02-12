from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sni.database import get_db

from . import service
from .schemas import QuoteCategoryBaseModel, QuoteCategoryModel

router = APIRouter()


@router.get("", response_model=List[QuoteCategoryBaseModel])
async def get_quote_categories(db: AsyncSession = Depends(get_db)):
    return await service.get_all(db_session=db)


@router.get("/{slug}", response_model=QuoteCategoryModel)
async def get_quote_category(slug: str, db: AsyncSession = Depends(get_db)):
    category = await service.get_category(slug, db_session=db)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    quotes = await service.get_category_quotes(category.slug, db_session=db)

    return {"category": category, "quotes": quotes}
