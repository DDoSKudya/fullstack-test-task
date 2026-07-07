from collections.abc import AsyncIterator
from pathlib import Path

import aiofiles
from starlette.datastructures import UploadFile

CHUNK_SIZE = 256 * 1024
HEADER_SIZE = 8192


class FileTooLargeError(Exception):
    def __init__(self, max_bytes: int) -> None:
        super().__init__(f"file exceeds maximum upload size of {max_bytes} bytes")


def resolve_path(root: Path, stored_name: str) -> Path:
    base = root.resolve()
    path = (base / stored_name).resolve()
    if not path.is_relative_to(base):
        raise ValueError("invalid stored name")
    return path


async def save_stream(upload: UploadFile, dest: Path, max_bytes: int) -> int:
    size = 0
    try:
        async with aiofiles.open(dest, "wb") as out:
            while chunk := await upload.read(CHUNK_SIZE):
                size += len(chunk)
                if size > max_bytes:
                    raise FileTooLargeError(max_bytes)
                await out.write(chunk)
    except FileTooLargeError:
        dest.unlink(missing_ok=True)
        raise
    return size


async def read_header(path: Path, size: int = HEADER_SIZE) -> bytes:
    async with aiofiles.open(path, "rb") as file:
        return await file.read(size)  # type: ignore[no-any-return]


async def iter_chunks(path: Path, chunk_size: int = CHUNK_SIZE) -> AsyncIterator[bytes]:
    async with aiofiles.open(path, "rb") as file:
        while chunk := await file.read(chunk_size):
            yield chunk
