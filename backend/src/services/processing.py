from pathlib import Path

import structlog
from sqlalchemy import select
from src.config import settings
from src.db.models import Alert, StoredFile
from src.db.session import get_session
from src.processing.metadata import extract_metadata
from src.processing.rules import ScanContext, detect_extension, run_scan
from src.services.alerts import create_alert_for_file
from src.storage.local import read_header, resolve_path

logger = structlog.get_logger()


async def run_pipeline(file_id: str) -> str | None:
    structlog.contextvars.bind_contextvars(file_id=file_id)
    session = get_session()
    file_item = await session.get(StoredFile, file_id)
    if file_item is None:
        return None

    if file_item.processing_status == "processed":
        return "processed"

    existing = await session.execute(select(Alert.id).where(Alert.file_id == file_id).limit(1))
    if existing.scalar_one_or_none() is not None:
        return file_item.processing_status

    file_item.processing_status = "processing"
    await session.flush()

    stored_path = resolve_path(Path(settings.storage_path), file_item.stored_name)
    if not stored_path.exists():
        file_item.processing_status = "failed"
        file_item.scan_status = file_item.scan_status or "failed"
        file_item.scan_details = "stored file not found during metadata extraction"
        create_alert_for_file(file_item)
        return "failed"

    header = await read_header(stored_path)
    ctx = ScanContext(
        extension=Path(file_item.original_name).suffix.lower(),
        declared_mime=file_item.mime_type,
        size=file_item.size,
        scan_max_bytes=settings.scan_max_bytes,
        detected_extension=detect_extension(header),
    )
    scan_status, scan_details, requires_attention = run_scan(ctx)
    file_item.scan_status = scan_status
    file_item.scan_details = scan_details
    file_item.requires_attention = requires_attention
    reasons_count = max(1, scan_details.count(", ") + 1) if requires_attention else 0
    logger.info(
        "scan.completed",
        scan_status=scan_status,
        reasons_count=reasons_count,
    )

    file_item.metadata_json = await extract_metadata(
        stored_path,
        file_item.mime_type,
        file_item.original_name,
        file_item.size,
    )
    file_item.processing_status = "processed"
    create_alert_for_file(file_item)
    return "processed"
