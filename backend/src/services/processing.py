from pathlib import Path

import structlog
from sqlalchemy import select
from src.config import settings
from src.db.models import Alert, StoredFile
from src.db.session import get_session
from src.processing.metadata import extract_metadata
from src.processing.rules import ScanContext, run_scan
from src.services.alerts import create_alert_for_file
from src.storage.local import resolve_path

logger = structlog.get_logger()


async def run_pipeline(file_id: str) -> None:
    structlog.contextvars.bind_contextvars(file_id=file_id)
    session = get_session()
    file_item = await session.get(StoredFile, file_id)
    if file_item is None:
        return

    existing = await session.execute(select(Alert).where(Alert.file_id == file_id))
    if existing.scalar_one_or_none() is not None:
        return

    file_item.processing_status = "processing"
    await session.flush()

    ctx = ScanContext(
        extension=Path(file_item.original_name).suffix.lower(),
        declared_mime=file_item.mime_type,
        size=file_item.size,
        scan_max_bytes=settings.scan_max_bytes,
    )
    scan_status, scan_details, requires_attention = run_scan(ctx)
    file_item.scan_status = scan_status
    file_item.scan_details = scan_details
    file_item.requires_attention = requires_attention
    logger.info("scan.completed", scan_status=scan_status, requires_attention=requires_attention)

    stored_path = resolve_path(Path(settings.storage_path), file_item.stored_name)
    if not stored_path.exists():
        file_item.processing_status = "failed"
        file_item.scan_status = file_item.scan_status or "failed"
        file_item.scan_details = "stored file not found during metadata extraction"
        create_alert_for_file(file_item)
        return

    file_item.metadata_json = extract_metadata(
        stored_path,
        file_item.mime_type,
        file_item.original_name,
        file_item.size,
    )
    file_item.processing_status = "processed"
    create_alert_for_file(file_item)
