from io import BytesIO
from unittest.mock import AsyncMock

import pytest
from src.db.session import get_session, session_scope
from src.services import files as files_service
from starlette.datastructures import Headers, UploadFile


def make_upload(data: bytes, filename: str = "test.txt") -> UploadFile:
    return UploadFile(
        file=BytesIO(data),
        filename=filename,
        headers=Headers({"content-type": "text/plain"}),
    )


async def create_file_with_failing_flush(upload: UploadFile, monkeypatch) -> None:
    async with session_scope():
        session = get_session()
        monkeypatch.setattr(
            session,
            "flush",
            AsyncMock(side_effect=RuntimeError("db error")),
        )
        await files_service.create_file("title", upload)


async def test_create_file_removes_stored_file_on_db_failure(
    storage_path,
    monkeypatch,
) -> None:
    upload = make_upload(b"hello")

    with pytest.raises(RuntimeError, match="db error"):
        await create_file_with_failing_flush(upload, monkeypatch)

    if any(storage_path.iterdir()):
        pytest.fail("stored file was not removed")
