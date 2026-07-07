from pathlib import Path


def extract_metadata(
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
        content = path.read_text(encoding="utf-8", errors="ignore")
        metadata["line_count"] = len(content.splitlines())
        metadata["char_count"] = len(content)
    elif mime_type == "application/pdf":
        pdf_bytes = path.read_bytes()
        metadata["approx_page_count"] = max(pdf_bytes.count(b"/Type /Page"), 1)

    return metadata
