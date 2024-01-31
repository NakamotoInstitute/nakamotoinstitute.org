from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sni.database import get_db

from .schemas import SkepticModel
from .service import get_all

router = APIRouter()


@router.get("", response_model=List[SkepticModel])
async def get_skeptics(db: AsyncSession = Depends(get_db)):
    return await get_all(db_session=db)
