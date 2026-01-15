from typing import Any

from fastapi import APIRouter, HTTPException, status

from sni.shared.dependencies import DB
from sni.shared.schemas import ErrorModel

from . import service
from .schemas import (
    ForumPostBaseModel,
    ForumPostDetailModel,
    ForumPostModel,
    ForumPostSource,
    ForumThreadBaseModel,
    ForumThreadModel,
)

router = APIRouter()


@router.get(
    "",
    summary="Get all forum posts",
    response_model=list[ForumPostBaseModel],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "All posts"}},
)
async def get_forum_posts(db: DB) -> Any:
    return await service.get_all_posts(db_session=db)


@router.get(
    "/threads",
    summary="Get all forum threads",
    response_model=list[ForumThreadBaseModel],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "All threads"}},
)
async def get_forum_threads(db: DB) -> Any:
    return await service.get_threads(db_session=db)


@router.get(
    "/{source}",
    summary="Get forum posts by source",
    response_model=list[ForumPostModel],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "Posts by source"}},
)
async def get_forum_posts_by_source(source: ForumPostSource, db: DB) -> Any:
    return await service.get_posts_by_source(source, db_session=db)


@router.get(
    "/{source}/threads",
    summary="Get forum threads by source",
    response_model=list[ForumThreadBaseModel],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "Threads by source"}},
)
async def get_forum_threads_by_source(source: ForumPostSource, db: DB) -> Any:
    return await service.get_threads_by_source(source, db_session=db)


@router.get(
    "/{source}/threads/{thread_id}",
    summary="Get forum thread by ID",
    response_model=ForumThreadModel,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Thread with posts"},
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorModel,
            "description": "Forum thread not found",
        },
    },
)
async def get_forum_thread_by_source(
    source: ForumPostSource, thread_id: int, db: DB, satoshi: bool = False
) -> Any:
    """Returns thread with posts and previous/next navigation."""
    thread = await service.get_thread(thread_id, db_session=db)
    if not thread or thread.source != source:
        raise HTTPException(status_code=404, detail="Forum thread not found")

    posts = await service.get_thread_posts(source, thread_id, satoshi, db_session=db)

    previous_thread = await service.get_thread(thread_id - 1, db_session=db)
    next_thread = await service.get_thread(thread_id + 1, db_session=db)

    return {
        "thread": thread,
        "posts": posts,
        "previous": previous_thread,
        "next": next_thread,
    }


@router.get(
    "/{source}/{satoshi_id}",
    summary="Get forum post by Satoshi ID",
    response_model=ForumPostDetailModel,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Post with nav"},
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorModel,
            "description": "Forum post not found",
        },
    },
)
async def get_forum_post_by_source(
    source: ForumPostSource, satoshi_id: int, db: DB
) -> Any:
    """Returns post with previous/next navigation."""
    post = await service.get_post_by_source(source, satoshi_id, db_session=db)
    if not post:
        raise HTTPException(status_code=404, detail="Forum post not found")

    previous_post = await service.get_post(satoshi_id - 1, db_session=db)
    next_post = await service.get_post(satoshi_id + 1, db_session=db)

    return {"post": post, "previous": previous_post, "next": next_post}
