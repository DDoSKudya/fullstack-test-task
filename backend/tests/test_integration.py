from httpx import AsyncClient
from sqlalchemy import delete
from src.db.models import Alert, StoredFile
from src.db.session import get_session, session_scope
from src.services.processing import run_pipeline


async def reset_tables() -> None:
    async with session_scope():
        session = get_session()
        await session.execute(delete(Alert))
        await session.execute(delete(StoredFile))


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
