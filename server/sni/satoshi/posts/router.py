from typing import Any

from fastapi import APIRouter, HTTPException

from sni.shared.dependencies import DB

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


@router.get("", response_model=list[ForumPostBaseModel])
async def get_forum_posts(db: DB) -> Any:
    return await service.get_all_posts(db_session=db)


@router.get("/threads", response_model=list[ForumThreadBaseModel])
async def get_forum_threads(db: DB) -> Any:
    return await service.get_threads(db_session=db)


@router.get("/{source}", response_model=list[ForumPostModel])
async def get_forum_posts_by_source(source: ForumPostSource, db: DB) -> Any:
    return await service.get_posts_by_source(source, db_session=db)


@router.get("/{source}/threads", response_model=list[ForumThreadBaseModel])
async def get_forum_threads_by_source(source: ForumPostSource, db: DB) -> Any:
    return await service.get_threads_by_source(source, db_session=db)


@router.get("/{source}/threads/{thread_id}", response_model=ForumThreadModel)
async def get_forum_thread_by_source(
    source: ForumPostSource, thread_id: int, db: DB, satoshi: bool = False
) -> Any:
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


@router.get("/{source}/{satoshi_id}", response_model=ForumPostDetailModel)
async def get_forum_post_by_source(
    source: ForumPostSource, satoshi_id: int, db: DB
) -> Any:
    post = await service.get_post_by_source(source, satoshi_id, db_session=db)
    if not post:
        raise HTTPException(status_code=404, detail="Forum post not found")

    previous_post = await service.get_post(satoshi_id - 1, db_session=db)
    next_post = await service.get_post(satoshi_id + 1, db_session=db)

    return {"post": post, "previous": previous_post, "next": next_post}
