from typing import Any

from fastapi import APIRouter, HTTPException, status

from sni.shared.dependencies import DB
from sni.shared.schemas import Error

from . import service
from .schemas import (
    EmailDetail,
    EmailSource,
    EmailThread,
    EmailThreadBase,
    SatoshiEmail,
)

router = APIRouter()


@router.get(
    "",
    summary="Get all emails",
    response_model=list[SatoshiEmail],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "All emails"}},
)
async def get_emails(db: DB) -> Any:
    return await service.get_all_emails(db_session=db)


@router.get(
    "/threads",
    summary="Get all email threads",
    response_model=list[EmailThreadBase],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "All threads"}},
)
async def get_email_threads(db: DB) -> Any:
    return await service.get_threads(db_session=db)


@router.get(
    "/{source}",
    summary="Get emails by source",
    response_model=list[SatoshiEmail],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "Emails by source"}},
)
async def get_emails_by_source(source: EmailSource, db: DB) -> Any:
    return await service.get_satoshi_emails_by_source(source, db_session=db)


@router.get(
    "/{source}/threads",
    summary="Get email threads by source",
    response_model=list[EmailThreadBase],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "Threads by source"}},
)
async def get_email_threads_by_source(source: EmailSource, db: DB) -> Any:
    return await service.get_threads_by_source(source, db_session=db)


@router.get(
    "/{source}/threads/{thread_id}",
    summary="Get email thread by ID",
    response_model=EmailThread,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Thread with emails"},
        status.HTTP_404_NOT_FOUND: {
            "model": Error,
            "description": "Email thread not found",
        },
    },
)
async def get_email_thread_by_source(
    source: EmailSource, thread_id: int, db: DB, satoshi: bool = False
) -> Any:
    """Returns thread with emails and previous/next navigation."""
    thread = await service.get_thread(thread_id, db_session=db)
    if not thread or thread.source != source:
        raise HTTPException(status_code=404, detail="Email thread not found")

    emails = await service.get_thread_emails(source, thread_id, satoshi, db_session=db)

    previous_thread = await service.get_thread(thread_id - 1, db_session=db)
    next_thread = await service.get_thread(thread_id + 1, db_session=db)

    return {
        "thread": thread,
        "emails": emails,
        "previous": previous_thread,
        "next": next_thread,
    }


@router.get(
    "/{source}/{satoshi_id}",
    summary="Get email by Satoshi ID",
    response_model=EmailDetail,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Email with nav"},
        status.HTTP_404_NOT_FOUND: {
            "model": Error,
            "description": "Email not found",
        },
    },
)
async def get_email_by_source(source: EmailSource, satoshi_id: int, db: DB) -> Any:
    """Returns email with previous/next navigation."""
    email = await service.get_satoshi_email_by_source(source, satoshi_id, db_session=db)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")

    previous_email = await service.get_email(satoshi_id - 1, db_session=db)
    next_email = await service.get_email(satoshi_id + 1, db_session=db)

    return {"email": email, "previous": previous_email, "next": next_email}
