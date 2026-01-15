from typing import Any

from fastapi import APIRouter, HTTPException, status

from sni.shared.dependencies import DB
from sni.shared.schemas import ErrorModel

from . import service
from .schemas import QuoteCategoryBaseModel, QuoteCategoryModel

router = APIRouter()


@router.get(
    "",
    summary="Get all quote categories",
    response_model=list[QuoteCategoryBaseModel],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "All categories"}},
)
async def get_quote_categories(db: DB) -> Any:
    return await service.get_all(db_session=db)


@router.get(
    "/{slug}",
    summary="Get quote category by slug",
    response_model=QuoteCategoryModel,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Category with quotes"},
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorModel,
            "description": "Category not found",
        },
    },
)
async def get_quote_category(slug: str, db: DB) -> Any:
    """Returns category details with all quotes in that category."""
    category = await service.get_category(slug, db_session=db)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    quotes = await service.get_category_quotes(category.slug, db_session=db)

    return {"category": category, "quotes": quotes}
