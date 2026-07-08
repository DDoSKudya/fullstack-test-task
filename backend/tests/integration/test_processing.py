from httpx import AsyncClient
from sqlalchemy import select
from src.db.models import Alert, StoredFile
from src.db.session import get_session, session_scope
from src.services.processing import run_pipeline
from tests.helpers import reset_tables


async def test_pipeline_returns_none_for_unknown_file(storage_path) -> None:
    async with session_scope():
        result = await run_pipeline("00000000-0000-0000-0000-000000000000")

    assert result is None


async def test_pipeline_fails_when_stored_file_missing(
    client: AsyncClient,
    storage_path,
) -> None:
    await reset_tables()

    response = await client.post(
        "/api/v1/files",
        data={"title": "ghost"},
        files={"file": ("ghost.txt", b"data", "text/plain")},
    )
    assert response.status_code == 201
    file_id = response.json()["id"]

    stored_file = next(storage_path.iterdir())
    stored_file.unlink()

    async with session_scope():
        status = await run_pipeline(file_id)
        session = get_session()
        file_item = await session.get(StoredFile, file_id)
        result = await session.execute(select(Alert).where(Alert.file_id == file_id))
        alerts = list(result.scalars())

    assert status == "failed"
    assert file_item is not None
    assert file_item.processing_status == "failed"
    assert len(alerts) == 1
    assert alerts[0].level == "critical"
