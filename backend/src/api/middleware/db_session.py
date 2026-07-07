from collections.abc import Awaitable, Callable

from src.db.session import session_scope
from starlette.requests import Request
from starlette.responses import Response


async def db_session_middleware(
    req: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    async with session_scope():
        return await call_next(req)
