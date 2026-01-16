from typing import Any

from fastapi import APIRouter, HTTPException, Response, status

from sni.shared.dependencies import DB
from sni.shared.responses import RSSResponse
from sni.shared.schemas import Error

from . import service
from .feed import generate_podcast_feed
from .schemas import Episode, EpisodeParams, PodcastBase, PodcastDetail

router = APIRouter()


@router.get(
    "",
    summary="Get all podcasts",
    response_model=list[PodcastBase],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "All podcasts"}},
)
async def get_podcasts(db: DB) -> Any:
    return await service.get_podcasts(db_session=db)


@router.get(
    "/home",
    summary="Get featured podcasts",
    response_model=list[PodcastBase],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "Featured podcasts"}},
)
async def get_home_podcasts(db: DB) -> Any:
    return await service.get_home_podcasts(db_session=db)


@router.get(
    "/episodes",
    summary="Get all episodes",
    response_model=list[EpisodeParams],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "All episodes"}},
)
async def get_episodes(db: DB) -> Any:
    return await service.get_episodes(db_session=db)


@router.get(
    "/{podcast_slug}/feed",
    summary="Get podcast RSS feed",
    response_class=Response,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "RSS feed",
            "content": {"application/rss+xml": {"schema": {"type": "string"}}},
        },
        status.HTTP_404_NOT_FOUND: {
            "model": Error,
            "description": "Podcast not found",
        },
    },
)
async def generate_feed(podcast_slug: str, db: DB) -> Response:
    """Returns 404 if podcast not found or has external feed."""
    podcast = await service.get_podcast_by_slug(podcast_slug, db_session=db)
    if not podcast or podcast.external_feed:
        raise HTTPException(status_code=404, detail="Podcast not found")

    feed = generate_podcast_feed(podcast)

    return RSSResponse(content=feed.rss_str(pretty=True))


@router.get(
    "/{podcast_slug}",
    summary="Get podcast by slug",
    response_model=PodcastDetail,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Podcast with episodes"},
        status.HTTP_404_NOT_FOUND: {
            "model": Error,
            "description": "Podcast not found",
        },
    },
)
async def get_podcast(podcast_slug: str, db: DB) -> Any:
    podcast = await service.get_podcast_by_slug(podcast_slug, db_session=db)
    if not podcast:
        raise HTTPException(status_code=404, detail="Podcast not found")

    return podcast


@router.get(
    "/{podcast_slug}/{episode_slug}",
    summary="Get episode by slug",
    response_model=Episode,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Episode details"},
        status.HTTP_404_NOT_FOUND: {
            "model": Error,
            "description": "Episode not found",
        },
    },
)
async def get_episode(podcast_slug: str, episode_slug: str, db: DB) -> Any:
    episode = await service.get_episode_by_slug(episode_slug, db_session=db)
    if not episode or episode.podcast.slug != podcast_slug:
        raise HTTPException(status_code=404, detail="Episode not found")

    return episode
