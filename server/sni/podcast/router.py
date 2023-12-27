from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from sni.database import get_db

from .schemas import EpisodeModel
from .service import get, get_all

router = APIRouter()


@router.get("", response_model=List[EpisodeModel])
def get_episodes(db: Session = Depends(get_db)):
    return get_all(db_session=db)


@router.get("/{slug}", response_model=EpisodeModel)
def get_episode(slug: str, db: Session = Depends(get_db)):
    episode = get(slug, db_session=db)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")

    return episode
