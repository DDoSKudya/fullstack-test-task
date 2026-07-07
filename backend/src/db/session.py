from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from src.config import settings

_engine_kwargs: dict[str, object] = {}
if settings.testing:
    _engine_kwargs["poolclass"] = NullPool
else:
    _engine_kwargs["pool_pre_ping"] = True

engine = create_async_engine(settings.database_url, **_engine_kwargs)
session_factory = async_sessionmaker(engine, expire_on_commit=False)

_session_ctx: ContextVar[AsyncSession | None] = ContextVar("db_session", default=None)
_after_commit_key = "after_commit"

AfterCommitHook = Callable[[], Awaitable[None]]


def get_session() -> AsyncSession:
    session = _session_ctx.get()
    if session is None:
        raise RuntimeError("Database session is not open. Use session_scope().")
    return session


def schedule_after_commit(hook: AfterCommitHook) -> None:
    hooks = get_session().info.setdefault(_after_commit_key, [])
    hooks.append(hook)


@asynccontextmanager
async def session_scope() -> AsyncIterator[AsyncSession]:
    session = session_factory()
    token = _session_ctx.set(session)
    session.info[_after_commit_key] = []
    try:
        yield session
        await session.commit()
        for hook in session.info[_after_commit_key]:
            await hook()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
        _session_ctx.reset(token)
