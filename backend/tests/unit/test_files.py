from unittest.mock import AsyncMock

import pytest
from sqlalchemy.exc import SQLAlchemyError
from src.db.session import get_session, session_scope
from src.services import files as files_service
from src.services.files import resolve_title
from tests.helpers import make_upload


async def create_file_with_failing_flush(upload, monkeypatch) -> None:
    async with session_scope():
        session = get_session()
        monkeypatch.setattr(
            session,
            "flush",
            AsyncMock(side_effect=SQLAlchemyError("db error")),
        )
        await files_service.create_file("title", upload)


async def test_create_file_removes_stored_file_on_db_failure(
    storage_path,
    monkeypatch,
) -> None:
    upload = make_upload(b"hello")

    with pytest.raises(SQLAlchemyError, match="db error"):
        await create_file_with_failing_flush(upload, monkeypatch)

    if any(storage_path.iterdir()):
        pytest.fail("stored file was not removed")


def test_resolve_title_uses_value_when_provided() -> None:
    assert resolve_title("  My doc  ") == "My doc"


def test_resolve_title_generates_token_when_empty() -> None:
    title = resolve_title("")
    assert len(title) == 8
    assert all(ch in "0123456789abcdef" for ch in title)


def test_resolve_title_generates_token_for_whitespace() -> None:
    title = resolve_title("   ")
    assert len(title) == 8


def test_resolve_title_tokens_are_unique() -> None:
    titles = {resolve_title("") for _ in range(20)}
    assert len(titles) > 1
