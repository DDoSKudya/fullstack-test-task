from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.config import settings

engine = create_async_engine(settings.database_url, pool_pre_ping=True)
session_factory = async_sessionmaker(engine, expire_on_commit=False)

_session_ctx: ContextVar[AsyncSession | None] = ContextVar("db_session", default=None)


def get_session() -> AsyncSession:
    session = _session_ctx.get()
    if session is None:
        raise RuntimeError("Database session is not open. Use session_scope().")
    return session


@asynccontextmanager
async def session_scope() -> AsyncIterator[AsyncSession]:
    session = session_factory()
    token = _session_ctx.set(session)
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
        _session_ctx.reset(token)
