from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles

from sni.authors.router import router as authors_router
from sni.content.update import update_content
from sni.library.router import router as library_router
from sni.mempool.router import router as mempool_router
from sni.podcasts.router import router as podcast_router
from sni.satoshi.router import router as satoshi_router
from sni.skeptics.router import router as skeptics_router

from .config import settings
from .constants import STATIC_ROUTE
from .middleware import APIKeyMiddleware


def generate_operation_id(route: APIRoute) -> str:
    """Generate clean operationIds for SDK generation.

    Produces IDs like 'authors-get_all' instead of 'get_authors_authors_get'.
    """
    tag = route.tags[0] if route.tags else "default"
    return f"{tag}-{route.name}"


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.ENVIRONMENT.is_debug:
        update_content()
    yield


app = FastAPI(lifespan=lifespan, generate_unique_id_function=generate_operation_id)

if settings.API_KEY:
    app.add_middleware(APIKeyMiddleware)


if settings.ENVIRONMENT.is_debug:
    app.mount(STATIC_ROUTE, StaticFiles(directory="static"), name="static")


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(authors_router, tags=["authors"], prefix="/authors")
app.include_router(library_router, tags=["library"], prefix="/library")
app.include_router(mempool_router, tags=["mempool"], prefix="/mempool")
app.include_router(podcast_router, tags=["podcasts"], prefix="/podcasts")
app.include_router(satoshi_router, tags=["satoshi"], prefix="/satoshi")
app.include_router(skeptics_router, tags=["skeptics"], prefix="/skeptics")
