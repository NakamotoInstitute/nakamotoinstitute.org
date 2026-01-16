from typing import Any

from fastapi import APIRouter, HTTPException, status

from sni.shared.dependencies import DB, Locale
from sni.shared.schemas import Error, SlugParam

from . import service
from .schemas import (
    Document,
    DocumentIndex,
    DocumentNode,
    DocumentNodeParams,
)

router = APIRouter()


@router.get(
    "",
    summary="Get all documents",
    response_model=list[DocumentIndex],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "All documents"}},
)
async def get_library_docs(locale: Locale, db: DB) -> Any:
    return await service.get_all_by_locale(db_session=db, locale=locale)


@router.get(
    "/params",
    summary="Get document params",
    response_model=list[SlugParam],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "Doc slugs for SSG"}},
)
async def get_library_params(db: DB) -> Any:
    """Get document slugs for static site generation."""
    return await service.get_params(db_session=db)


@router.get(
    "/params/nodes",
    summary="Get document node params",
    response_model=list[DocumentNodeParams],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "Node slugs for SSG"}},
)
async def get_library_node_params(db: DB) -> Any:
    """Get document node slugs for static site generation."""
    return await service.get_node_params(db_session=db)


@router.get(
    "/home",
    summary="Get featured documents",
    response_model=list[DocumentIndex],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "Featured docs"}},
)
async def get_home_library_docs(locale: Locale, db: DB) -> Any:
    """Returns Bitcoin whitepaper, Shelling Out, and Cypherpunk Manifesto."""
    result = await service.get_some_by_slugs_and_locale(
        ["bitcoin", "shelling-out", "cypherpunk-manifesto"],
        db_session=db,
        locale=locale,
    )
    return result


@router.get(
    "/{slug}",
    summary="Get document by slug",
    response_model=Document,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Document with content"},
        status.HTTP_404_NOT_FOUND: {
            "model": Error,
            "description": "Document not found",
        },
    },
)
async def get_library_doc(slug: str, locale: Locale, db: DB) -> Any:
    doc = await service.get(slug, db_session=db, locale=locale)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    return doc


@router.get(
    "/{doc_slug}/{slug}",
    summary="Get document node by slug",
    response_model=DocumentNode,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Document section"},
        status.HTTP_404_NOT_FOUND: {
            "model": Error,
            "description": "Document node not found",
        },
    },
)
async def get_library_doc_node(slug: str, doc_slug: str, locale: Locale, db: DB) -> Any:
    """Get a section or chapter within a document."""
    node = await service.get_node(slug, doc_slug=doc_slug, db_session=db, locale=locale)
    if not node:
        raise HTTPException(status_code=404, detail="Document node not found")

    return node
