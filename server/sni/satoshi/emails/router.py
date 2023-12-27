from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from sni.database import get_db

from .schemas import (
    EmailBaseModel,
    EmailDetailModel,
    EmailThreadBaseModel,
    EmailThreadModel,
    SatoshiEmailModel,
)
from .service import (
    get_all_emails,
    get_email,
    get_satoshi_email_by_source,
    get_satoshi_emails_by_source,
    get_thread,
    get_thread_emails,
    get_threads,
    get_threads_by_source,
)

router = APIRouter()


@router.get("", response_model=List[EmailBaseModel])
def get_emails(db: Session = Depends(get_db)):
    return get_all_emails(db_session=db)


@router.get("/threads", response_model=List[EmailThreadBaseModel])
def get_email_threads(db: Session = Depends(get_db)):
    return get_threads(db_session=db)


@router.get("/{source}", response_model=List[SatoshiEmailModel])
def get_emails_by_source(source: str, db: Session = Depends(get_db)):
    return get_satoshi_emails_by_source(source, db_session=db)


@router.get("/{source}/threads", response_model=List[EmailThreadBaseModel])
def get_email_threads_by_source(source: str, db: Session = Depends(get_db)):
    return get_threads_by_source(source, db_session=db)


@router.get(
    "/{source}/threads/{thread_id}",
    response_model=EmailThreadModel,
)
def get_email_thread_by_source(
    source: str, thread_id: int, satoshi: bool = False, db: Session = Depends(get_db)
):
    emails = get_thread_emails(source, thread_id, satoshi, db_session=db)
    if not emails:
        raise HTTPException(status_code=404, detail="Email thread not found")
    thread = emails[0].thread

    previous_thread = get_thread(thread_id - 1, db_session=db)
    next_thread = get_thread(thread_id + 1, db_session=db)

    return {
        "emails": emails,
        "thread": thread,
        "previous": previous_thread,
        "next": next_thread,
    }


@router.get("/{source}/{satoshi_id}", response_model=EmailDetailModel)
def get_email_by_source(source: str, satoshi_id: int, db: Session = Depends(get_db)):
    email = get_satoshi_email_by_source(source, satoshi_id, db_session=db)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")

    previous_email = get_email(satoshi_id - 1, db_session=db)
    next_email = get_email(satoshi_id + 1, db_session=db)

    return {"email": email, "previous": previous_email, "next": next_email}
