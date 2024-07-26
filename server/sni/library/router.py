from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sni.constants import LocaleType
from sni.database import get_db
from sni.shared.schemas import SlugParamModel

from . import service
from .schemas import (
    DocumentIndexModel,
    DocumentModel,
    DocumentNodeModel,
    DocumentNodeParamsModel,
)

router = APIRouter()


@router.get("", response_model=list[DocumentIndexModel])
async def get_library_docs(
    locale: LocaleType = "en", db: AsyncSession = Depends(get_db)
) -> Any:
    return await service.get_all_by_locale(db_session=db, locale=locale)


@router.get("/params", response_model=list[SlugParamModel])
async def get_library_params(db: AsyncSession = Depends(get_db)) -> Any:
    return await service.get_params(db_session=db)


@router.get("/params/nodes", response_model=list[DocumentNodeParamsModel])
async def get_library_node_params(db: AsyncSession = Depends(get_db)) -> Any:
    return await service.get_node_params(db_session=db)


@router.get("/home", response_model=list[DocumentIndexModel])
async def get_home_library_docs(
    locale: LocaleType = "en", db: AsyncSession = Depends(get_db)
) -> Any:
    result = await service.get_some_by_slugs_and_locale(
        ["bitcoin", "shelling-out", "cypherpunk-manifesto"],
        db_session=db,
        locale=locale,
    )
    return result


@router.get("/{slug}", response_model=DocumentModel)
async def get_library_doc(
    slug: str, locale: LocaleType = "en", db: AsyncSession = Depends(get_db)
) -> Any:
    doc = await service.get(slug, db_session=db, locale=locale)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    return doc


@router.get("/{doc_slug}/{slug}", response_model=DocumentNodeModel)
async def get_library_doc_node(
    slug: str,
    doc_slug: str,
    locale: LocaleType = "en",
    db: AsyncSession = Depends(get_db),
) -> Any:
    node = await service.get_node(slug, doc_slug=doc_slug, db_session=db, locale=locale)
    if not node:
        raise HTTPException(status_code=404, detail="Document node not found")

    return node
