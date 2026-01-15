from typing import Any

from fastapi import APIRouter, status

from sni.shared.dependencies import DB

from .schemas import SkepticModel
from .service import get_all

router = APIRouter()


@router.get(
    "",
    summary="Get all skeptics",
    response_model=list[SkepticModel],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "All skeptics"}},
)
async def get_skeptics(db: DB) -> Any:
    """Returns all Bitcoin skeptic predictions."""
    return await get_all(db_session=db)
