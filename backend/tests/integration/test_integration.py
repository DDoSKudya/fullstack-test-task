from httpx import AsyncClient
from src.db.session import session_scope
from src.services.processing import run_pipeline
from tests.helpers import reset_tables


async def test_upload_and_pipeline_creates_info_alert(
    client: AsyncClient,
    storage_path,
) -> None:
    await reset_tables()

    response = await client.post(
        "/api/v1/files",
        data={"title": "notes"},
        files={"file": ("readme.txt", b"line one\nline two", "text/plain")},
    )
    assert response.status_code == 201
    file_id = response.json()["id"]

    async with session_scope():
        await run_pipeline(file_id)

    alerts_response = await client.get("/api/v1/alerts")
    assert alerts_response.status_code == 200
    alerts = alerts_response.json()
    assert len(alerts) == 1
    assert alerts[0]["file_id"] == file_id
    assert alerts[0]["level"] == "info"

    file_response = await client.get(f"/api/v1/files/{file_id}")
    body = file_response.json()
    assert body["processing_status"] == "processed"
    assert body["scan_status"] == "clean"
    assert body["metadata_json"]["line_count"] == 2


async def test_suspicious_file_creates_warning_alert(
    client: AsyncClient,
    storage_path,
) -> None:
    await reset_tables()

    response = await client.post(
        "/api/v1/files",
        data={"title": "binary"},
        files={"file": ("malware.exe", b"MZ", "application/octet-stream")},
    )
    assert response.status_code == 201
    file_id = response.json()["id"]

    async with session_scope():
        await run_pipeline(file_id)

    alerts_response = await client.get("/api/v1/alerts")
    alerts = alerts_response.json()
    assert alerts[0]["level"] == "warning"
    assert "suspicious extension" in alerts[0]["message"]

    file_response = await client.get(f"/api/v1/files/{file_id}")
    assert file_response.json()["requires_attention"] is True


async def test_pipeline_is_idempotent(client: AsyncClient, storage_path) -> None:
    await reset_tables()

    response = await client.post(
        "/api/v1/files",
        data={"title": "once"},
        files={"file": ("once.txt", b"data", "text/plain")},
    )
    file_id = response.json()["id"]

    async with session_scope():
        await run_pipeline(file_id)
        await run_pipeline(file_id)

    alerts_response = await client.get("/api/v1/alerts")
    assert len(alerts_response.json()) == 1


async def test_delete_file_cascades_alerts(client: AsyncClient, storage_path) -> None:
    await reset_tables()

    response = await client.post(
        "/api/v1/files",
        data={"title": "temp"},
        files={"file": ("temp.txt", b"data", "text/plain")},
    )
    file_id = response.json()["id"]

    async with session_scope():
        await run_pipeline(file_id)

    delete_response = await client.delete(f"/api/v1/files/{file_id}")
    assert delete_response.status_code == 204

    file_response = await client.get(f"/api/v1/files/{file_id}")
    assert file_response.status_code == 404

    alerts_response = await client.get("/api/v1/alerts")
    assert alerts_response.json() == []


async def test_upload_without_title_generates_token(client: AsyncClient, storage_path) -> None:
    await reset_tables()

    response = await client.post(
        "/api/v1/files",
        data={"title": ""},
        files={"file": ("doc.txt", b"data", "text/plain")},
    )
    assert response.status_code == 201
    title = response.json()["title"]
    assert len(title) == 8
    assert all(ch in "0123456789abcdef" for ch in title)


async def test_download_file_returns_content(client: AsyncClient, storage_path) -> None:
    await reset_tables()

    response = await client.post(
        "/api/v1/files",
        data={"title": "doc"},
        files={"file": ("readme.txt", b"hello world", "text/plain")},
    )
    assert response.status_code == 201
    file_id = response.json()["id"]

    download = await client.get(f"/api/v1/files/{file_id}/download")
    assert download.status_code == 200
    assert download.content == b"hello world"


async def test_list_files_pagination(client: AsyncClient, storage_path) -> None:
    await reset_tables()

    for index in range(3):
        response = await client.post(
            "/api/v1/files",
            data={"title": f"file-{index}"},
            files={"file": (f"f{index}.txt", b"x", "text/plain")},
        )
        assert response.status_code == 201

    all_files = await client.get("/api/v1/files")
    assert len(all_files.json()) == 3

    page = await client.get("/api/v1/files", params={"limit": 2, "offset": 0})
    assert page.status_code == 200
    assert len(page.json()) == 2
