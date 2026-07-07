import asyncio
from pathlib import Path

from pypdf import PdfReader
from src.storage.local import CHUNK_SIZE, iter_chunks


async def text_stats(path: Path, chunk_size: int = CHUNK_SIZE) -> tuple[int, int]:
    lines = 0
    chars = 0
    trailing_nl = True
    async for chunk in iter_chunks(path, chunk_size):
        chars += len(chunk)
        lines += chunk.count(b"\n")
        trailing_nl = chunk.endswith(b"\n")
    if chars and not trailing_nl:
        lines += 1
    return lines, chars


def pdf_page_count(path: Path) -> int:
    with path.open("rb") as fh:
        return len(PdfReader(fh, strict=False).pages)


async def extract_metadata(
    path: Path,
    mime_type: str,
    original_name: str,
    size: int,
) -> dict[str, object]:
    metadata: dict[str, object] = {
        "extension": Path(original_name).suffix.lower(),
        "size_bytes": size,
        "mime_type": mime_type,
    }

    if mime_type.startswith("text/"):
        line_count, char_count = await text_stats(path)
        metadata["line_count"] = line_count
        metadata["char_count"] = char_count
    elif mime_type == "application/pdf":
        metadata["approx_page_count"] = await asyncio.to_thread(pdf_page_count, path)

    return metadata
