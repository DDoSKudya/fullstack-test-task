import os

os.environ["TESTING"] = "1"

from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient
from src.config import settings
from src.main import app


@pytest.fixture
def storage_path(tmp_path, monkeypatch):
    path = tmp_path / "files"
    path.mkdir()
    monkeypatch.setattr(settings, "storage_path", str(path))
    return path


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True)
def noop_enqueue(monkeypatch):
    async def _noop(file_id: str) -> None:
        del file_id

    monkeypatch.setattr("src.worker.tasks.process_file.kiq", _noop)
