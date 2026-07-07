from io import BytesIO
from pathlib import Path

import pytest
from src.storage.local import (
    CHUNK_SIZE,
    FileTooLargeError,
    delete_path,
    iter_chunks,
    resolve_path,
    save_stream,
)
from starlette.datastructures import Headers, UploadFile


def make_upload(data: bytes, filename: str = "test.txt") -> UploadFile:
    return UploadFile(
        file=BytesIO(data),
        filename=filename,
        headers=Headers({"content-type": "text/plain"}),
    )


async def test_save_stream_writes_file(tmp_path: Path) -> None:
    payload = b"hello"
    dest = tmp_path / "stored.bin"

    size = await save_stream(make_upload(payload), dest, max_bytes=1024)

    assert size == len(payload)
    assert dest.read_bytes() == payload


async def test_save_stream_rejects_oversized_file(tmp_path: Path) -> None:
    payload = b"x" * (CHUNK_SIZE + 1)
    dest = tmp_path / "big.bin"

    with pytest.raises(FileTooLargeError):
        await save_stream(make_upload(payload), dest, max_bytes=CHUNK_SIZE)

    assert not dest.exists()


async def test_iter_chunks_reads_in_parts(tmp_path: Path) -> None:
    payload = b"a" * (CHUNK_SIZE + 10)
    path = tmp_path / "chunked.bin"
    path.write_bytes(payload)

    parts: list[bytes] = []
    async for chunk in iter_chunks(path, chunk_size=CHUNK_SIZE):
        parts.append(chunk)

    assert b"".join(parts) == payload
    assert len(parts) == 2


def test_resolve_path_blocks_traversal(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="invalid stored name"):
        resolve_path(tmp_path, "../outside.txt")


def test_delete_path_removes_file(tmp_path: Path) -> None:
    path = tmp_path / "remove.me"
    path.write_bytes(b"data")

    delete_path(path)

    assert not path.exists()
