from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from sni.database import get_db

from .schemas import SkepticModel
from .service import get_all

router = APIRouter()


@router.get("", response_model=List[SkepticModel])
def get_skeptics(db: Session = Depends(get_db)):
    return get_all(db_session=db)
