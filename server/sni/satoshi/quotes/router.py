from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from sni.database import get_db

from .schemas import QuoteCategoryBaseModel, QuoteCategoryModel
from .service import get, get_all

router = APIRouter()


@router.get("", response_model=List[QuoteCategoryBaseModel])
def get_quote_categories(db: Session = Depends(get_db)):
    return get_all(db_session=db)


@router.get("/{slug}", response_model=QuoteCategoryModel)
def get_quote_category(slug: str, db: Session = Depends(get_db)):
    category = get(slug, db_session=db)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return {"category": category, "quotes": category.quotes}
