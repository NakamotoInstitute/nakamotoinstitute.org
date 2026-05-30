from fastapi import APIRouter, status

from sni.shared.dependencies import DB, Locale

from . import service
from .schemas import SearchResponse

router = APIRouter()


@router.get(
    "",
    summary="Site-wide search",
    response_model=SearchResponse,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "Search results"}},
)
async def search(
    q: str,
    locale: Locale,
    db: DB,
    category: str | None = None,
    page: int = 1,
) -> SearchResponse:
    result = await service.search(
        db_session=db,
        q=q,
        locale=locale,
        category=category,
        page=page,
    )
    return SearchResponse.model_validate(result)
