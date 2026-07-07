import time
from collections.abc import Awaitable, Callable

import structlog
from starlette.requests import Request
from starlette.responses import Response

logger = structlog.get_logger()
_SKIP_PATHS = {"/health", "/ready"}


async def http_logging_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    path = request.url.path
    if path in _SKIP_PATHS:
        return await call_next(request)

    started = time.perf_counter()
    logger.info("http.request.started", method=request.method, path=path)
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - started) * 1000, 2)
    logger.info(
        "http.request.completed",
        method=request.method,
        path=path,
        status_code=response.status_code,
        duration_ms=duration_ms,
    )
    return response
