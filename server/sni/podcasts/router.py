from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from sni.database import get_db
from sni.shared.responses import RSSResponse

from . import service
from .feed import generate_podcast_feed
from .schemas import BasePodcastModel, EpisodeModel, EpisodeParams, PodcastDetailModel

router = APIRouter()


@router.get("", response_model=list[BasePodcastModel])
async def get_podcasts(db: AsyncSession = Depends(get_db)) -> Any:
    return await service.get_podcasts(db_session=db)


@router.get("/home", response_model=list[BasePodcastModel])
async def get_home_podcasts(db: AsyncSession = Depends(get_db)) -> Any:
    return await service.get_home_podcasts(db_session=db)


@router.get("/episodes", response_model=list[EpisodeParams])
async def get_episodes(db: AsyncSession = Depends(get_db)) -> Any:
    return await service.get_episodes(db_session=db)


@router.get("/{podcast_slug}/feed", response_class=Response)
async def generate_feed(
    podcast_slug: str, db: AsyncSession = Depends(get_db)
) -> Response:
    podcast = await service.get_podcast_by_slug(podcast_slug, db_session=db)
    if not podcast or podcast.external_feed:
        raise HTTPException(status_code=404, detail="Podcast not found")

    feed = generate_podcast_feed(podcast)

    return RSSResponse(content=feed.rss_str(pretty=True))


@router.get("/{podcast_slug}", response_model=PodcastDetailModel)
async def get_podcast(podcast_slug: str, db: AsyncSession = Depends(get_db)) -> Any:
    podcast = await service.get_podcast_by_slug(podcast_slug, db_session=db)
    if not podcast:
        raise HTTPException(status_code=404, detail="Podcast not found")

    return podcast


@router.get("/{podcast_slug}/{episode_slug}", response_model=EpisodeModel)
async def get_episode(
    podcast_slug: str, episode_slug: str, db: AsyncSession = Depends(get_db)
) -> Any:
    episode = await service.get_episode_by_slug(episode_slug, db_session=db)
    if not episode or episode.podcast.slug != podcast_slug:
        raise HTTPException(status_code=404, detail="Episode not found")

    return episode
