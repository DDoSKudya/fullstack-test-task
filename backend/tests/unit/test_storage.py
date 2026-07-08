from pathlib import Path

import pytest
from src.storage.local import (
    CHUNK_SIZE,
    FileTooLargeError,
    iter_chunks,
    resolve_path,
    save_stream,
)
from tests.helpers import make_upload


async def test_save_stream_writes_file(tmp_path: Path) -> None:
    payload = b"hello"
    dest = tmp_path / "stored.bin"

    size = await save_stream(make_upload(payload), dest, max_bytes=1024)

    assert size == len(payload)
    assert dest.read_bytes() == payload


async def test_save_stream_accepts_payload_at_exact_limit(tmp_path: Path) -> None:
    payload = b"12345"
    dest = tmp_path / "exact.bin"

    size = await save_stream(make_upload(payload), dest, max_bytes=len(payload))

    assert size == len(payload)
    assert dest.exists()


async def test_save_stream_rejects_oversized_file(tmp_path: Path) -> None:
    payload = b"x" * (CHUNK_SIZE + 1)
    dest = tmp_path / "big.bin"

    with pytest.raises(FileTooLargeError, match="262144 bytes"):
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
