from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from sni.database import get_db
from sni.shared.responses import RSSResponse

from .feed import generate_podcast_feed
from .schemas import EpisodeModel
from .service import get, get_all

router = APIRouter()


@router.get("", response_model=List[EpisodeModel])
def get_episodes(db: Session = Depends(get_db)):
    return get_all(db_session=db)


@router.get("/feed", response_class=Response)
async def generate_feed(db: Session = Depends(get_db)):
    episodes = get_all(db_session=db)
    feed = generate_podcast_feed(episodes)

    return RSSResponse(content=feed.rss_str(pretty=True))


@router.get("/{slug}", response_model=EpisodeModel)
def get_episode(slug: str, db: Session = Depends(get_db)):
    episode = get(slug, db_session=db)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")

    return episode
