from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from sni.config import LocaleType
from sni.database import get_db
from sni.shared.schemas import SlugParamModel

from .schemas import DocumentIndexModel, DocumentModel
from .service import get, get_all, get_all_by_locale

router = APIRouter()


@router.get("", response_model=List[DocumentIndexModel])
def get_library_docs(locale: LocaleType = "en", db: Session = Depends(get_db)):
    return get_all_by_locale(db_session=db, locale=locale)


@router.get("/params", response_model=List[SlugParamModel])
def get_library_params(db: Session = Depends(get_db)):
    docs = get_all(db_session=db)
    return [{"locale": doc.locale, "slug": doc.slug} for doc in docs]


@router.get("/{slug}", response_model=DocumentModel)
def get_library_doc(
    slug: str, locale: LocaleType = "en", db: Session = Depends(get_db)
):
    doc = get(slug, db_session=db, locale=locale)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    return doc
