from fastapi import APIRouter, HTTPException

from sni.shared.dependencies import DB

from . import service
from .schemas import QuoteCategoryBaseModel, QuoteCategoryModel

router = APIRouter()


@router.get("", response_model=list[QuoteCategoryBaseModel])
async def get_quote_categories(db: DB):
    return await service.get_all(db_session=db)


@router.get("/{slug}", response_model=QuoteCategoryModel)
async def get_quote_category(slug: str, db: DB):
    category = await service.get_category(slug, db_session=db)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    quotes = await service.get_category_quotes(category.slug, db_session=db)

    return {"category": category, "quotes": quotes}
