import pytest
from src.db.session import get_session, session_scope


async def test_get_session_outside_scope_raises() -> None:
    with pytest.raises(RuntimeError, match="session_scope"):
        get_session()


async def test_session_scope_exposes_same_session() -> None:
    async with session_scope() as outer:
        assert get_session() is outer
