from typing import Any

from fastapi import APIRouter

from sni.shared.dependencies import DB

from .schemas import SkepticModel
from .service import get_all

router = APIRouter()


@router.get("", response_model=list[SkepticModel])
async def get_skeptics(db: DB) -> Any:
    return await get_all(db_session=db)
