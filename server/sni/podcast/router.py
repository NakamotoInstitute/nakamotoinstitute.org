from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from sni.database import get_db
from sni.shared.responses import RSSResponse

from .feed import generate_podcast_feed
from .schemas import EpisodeModel
from .service import get, get_all

router = APIRouter()


@router.get("", response_model=list[EpisodeModel])
async def get_episodes(db: AsyncSession = Depends(get_db)) -> Any:
    return await get_all(db_session=db)


@router.get("/feed", response_class=Response)
async def generate_feed(db: AsyncSession = Depends(get_db)) -> Response:
    episodes = await get_all(db_session=db)
    feed = generate_podcast_feed(episodes)

    return RSSResponse(content=feed.rss_str(pretty=True))


@router.get("/{slug}", response_model=EpisodeModel)
async def get_episode(slug: str, db: AsyncSession = Depends(get_db)) -> Any:
    episode = await get(slug, db_session=db)
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")

    return episode
