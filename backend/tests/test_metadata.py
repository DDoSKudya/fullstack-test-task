from pathlib import Path

from src.processing.metadata import extract_metadata, pdf_page_count, text_stats
from src.processing.rules import detect_extension
from src.storage.local import CHUNK_SIZE

PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
    b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
    b"\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01"
    b"\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)

MINIMAL_PDF = b"""%PDF-1.1
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
3 0 obj<</Type/Page/MediaBox[0 0 3 3]/Parent 2 0 R>>endobj
xref
0 4
0000000000 65535 f 
0000000009 00000 n 
0000000052 00000 n 
0000000101 00000 n 
trailer<</Size 4/Root 1 0 R>>
startxref
178
%%EOF
"""


def test_detect_extension_png() -> None:
    assert detect_extension(PNG_BYTES) == "png"


def test_detect_extension_unknown() -> None:
    assert detect_extension(b"plain text file") is None


async def test_text_stats_counts_lines_and_chars(tmp_path: Path) -> None:
    path = tmp_path / "sample.txt"
    payload = b"aaa\nbbb\nccc"
    path.write_bytes(payload)

    lines, chars = await text_stats(path, chunk_size=4)

    assert lines == 3
    assert chars == len(payload)


async def test_text_stats_single_line_without_trailing_newline(tmp_path: Path) -> None:
    path = tmp_path / "one-line.txt"
    path.write_bytes(b"hello")

    lines, chars = await text_stats(path)

    assert lines == 1
    assert chars == 5


async def test_text_stats_uses_chunked_reads(tmp_path: Path) -> None:
    path = tmp_path / "chunked.txt"
    path.write_bytes(b"x" * (CHUNK_SIZE + 10))

    lines, chars = await text_stats(path, chunk_size=CHUNK_SIZE)

    assert lines == 1
    assert chars == CHUNK_SIZE + 10


def test_pdf_page_count_reads_pages(tmp_path: Path) -> None:
    path = tmp_path / "doc.pdf"
    path.write_bytes(MINIMAL_PDF)

    assert pdf_page_count(path) == 1


async def test_extract_metadata_for_text(tmp_path: Path) -> None:
    path = tmp_path / "notes.txt"
    path.write_text("alpha\nbeta", encoding="utf-8")

    metadata = await extract_metadata(path, "text/plain", "notes.txt", path.stat().st_size)

    assert metadata["line_count"] == 2
    assert metadata["char_count"] == 10


async def test_extract_metadata_for_pdf(tmp_path: Path) -> None:
    path = tmp_path / "doc.pdf"
    path.write_bytes(MINIMAL_PDF)

    metadata = await extract_metadata(
        path,
        "application/pdf",
        "doc.pdf",
        path.stat().st_size,
    )

    assert metadata["approx_page_count"] == 1
