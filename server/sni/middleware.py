from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from .config import settings
from .constants import STATIC_ROUTE


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/health":
            return await call_next(request)

        if settings.ENVIRONMENT.is_debug and request.url.path.startswith(STATIC_ROUTE):
            return await call_next(request)

        api_key = request.headers.get("X-API-Key") or request.query_params.get(
            "api_key"
        )
        if api_key != settings.API_KEY:
            return JSONResponse(
                {"detail": "Invalid or missing API key"}, status_code=401
            )

        return await call_next(request)
