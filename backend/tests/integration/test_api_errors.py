from httpx import AsyncClient
from sqlalchemy import delete
from src.config import settings
from src.db.models import Alert, StoredFile
from src.db.session import get_session, session_scope


async def reset_tables() -> None:
    async with session_scope():
        session = get_session()
        await session.execute(delete(Alert))
        await session.execute(delete(StoredFile))


async def test_upload_rejects_empty_file(client: AsyncClient, storage_path) -> None:
    await reset_tables()

    response = await client.post(
        "/api/v1/files",
        data={"title": "empty"},
        files={"file": ("empty.txt", b"", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "File is empty"


async def test_upload_rejects_missing_filename(client: AsyncClient, storage_path) -> None:
    await reset_tables()

    response = await client.post(
        "/api/v1/files",
        data={"title": "no-name"},
        files={"file": ("", b"data", "text/plain")},
    )

    assert response.status_code == 422


async def test_upload_rejects_oversized_file(
    client: AsyncClient,
    storage_path,
    monkeypatch,
) -> None:
    await reset_tables()
    monkeypatch.setattr(settings, "max_upload_mb", 0)

    response = await client.post(
        "/api/v1/files",
        data={"title": "big"},
        files={"file": ("big.txt", b"too large", "text/plain")},
    )

    assert response.status_code == 413
    assert "maximum upload size" in response.json()["detail"]


async def test_get_file_not_found(client: AsyncClient) -> None:
    response = await client.get("/api/v1/files/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json()["detail"] == "File not found"


async def test_delete_file_not_found(client: AsyncClient) -> None:
    response = await client.delete("/api/v1/files/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404


async def test_download_file_not_found(client: AsyncClient) -> None:
    response = await client.get("/api/v1/files/00000000-0000-0000-0000-000000000000/download")

    assert response.status_code == 404


async def test_list_files_rejects_invalid_pagination(client: AsyncClient) -> None:
    too_small = await client.get("/api/v1/files", params={"limit": 0})
    assert too_small.status_code == 422

    too_large = await client.get("/api/v1/files", params={"limit": 101})
    assert too_large.status_code == 422

    bad_offset = await client.get("/api/v1/files", params={"offset": -1})
    assert bad_offset.status_code == 422
