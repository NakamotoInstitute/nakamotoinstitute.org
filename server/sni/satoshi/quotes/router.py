from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sni.database import get_db

from .schemas import QuoteCategoryBaseModel, QuoteCategoryModel
from .service import get, get_all

router = APIRouter()


@router.get("", response_model=List[QuoteCategoryBaseModel])
async def get_quote_categories(db: AsyncSession = Depends(get_db)):
    return await get_all(db_session=db)


@router.get("/{slug}", response_model=QuoteCategoryModel)
async def get_quote_category(slug: str, db: AsyncSession = Depends(get_db)):
    category = await get(slug, db_session=db)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    QuoteCategoryModel.validate({"category": category, "quotes": category.quotes})

    return {"category": category, "quotes": category.quotes}
