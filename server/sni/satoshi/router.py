from fastapi import APIRouter

from .emails.router import router as emails_router
from .posts.router import router as posts_router
from .quotes.router import router as quotes_router

router = APIRouter()

router.include_router(emails_router, prefix="/emails")
router.include_router(posts_router, prefix="/posts")
router.include_router(quotes_router, prefix="/quotes")
