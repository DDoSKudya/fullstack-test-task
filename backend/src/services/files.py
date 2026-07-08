import mimetypes
import secrets
from pathlib import Path
from uuid import uuid4

import structlog
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from src.config import settings
from src.db.models import StoredFile
from src.db.session import get_session, schedule_after_commit
from src.storage.local import FileTooLargeError, resolve_path, save_stream
from starlette.datastructures import UploadFile

logger = structlog.get_logger()


def resolve_title(title: str) -> str:
    stripped = title.strip()
    return stripped or secrets.token_hex(4)


async def list_files(limit: int = 50, offset: int = 0) -> list[StoredFile]:
    result = await get_session().execute(
        select(StoredFile).order_by(StoredFile.created_at.desc()).limit(limit).offset(offset)
    )
    return list(result.scalars())


async def get_file(file_id: str) -> StoredFile:
    file_item = await get_session().get(StoredFile, file_id)
    if file_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return file_item


async def _enqueue_process_file(file_id: str) -> None:
    from src.worker.tasks import process_file

    await process_file.kiq(file_id)
    logger.info("task.enqueued", file_id=file_id)


async def create_file(title: str, upload_file: UploadFile) -> StoredFile:
    if not upload_file.filename:
        logger.warning("file.upload.failed", reason="filename required")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required",
        )

    logger.info("file.upload.started", original_name=upload_file.filename)

    file_id = str(uuid4())
    suffix = Path(upload_file.filename).suffix
    stored_name = f"{file_id}{suffix}"
    root = Path(settings.storage_path)
    root.mkdir(parents=True, exist_ok=True)
    dest = resolve_path(root, stored_name)

    try:
        size = await save_stream(upload_file, dest, settings.max_upload_bytes)
    except FileTooLargeError as exc:
        logger.warning("file.upload.failed", reason=str(exc))
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail=str(exc),
        ) from exc

    if size == 0:
        dest.unlink(missing_ok=True)
        logger.warning("file.upload.failed", reason="file is empty")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is empty")

    mime_type = (
        upload_file.content_type
        or mimetypes.guess_type(stored_name)[0]
        or "application/octet-stream"
    )
    file_item = StoredFile(
        id=file_id,
        title=resolve_title(title),
        original_name=upload_file.filename,
        stored_name=stored_name,
        mime_type=mime_type,
        size=size,
        processing_status="uploaded",
    )
    try:
        get_session().add(file_item)
        await get_session().flush()
    except SQLAlchemyError as exc:
        dest.unlink(missing_ok=True)
        logger.warning("file.upload.failed", reason=type(exc).__name__)
        raise

    logger.info("file.upload.completed", file_id=file_id, size_bytes=size)
    schedule_after_commit(lambda: _enqueue_process_file(file_id))

    return file_item


async def delete_file(file_id: str) -> None:
    file_item = await get_file(file_id)
    stored_path = resolve_path(Path(settings.storage_path), file_item.stored_name)
    stored_path.unlink(missing_ok=True)
    await get_session().delete(file_item)


async def get_file_path(file_id: str) -> tuple[StoredFile, Path]:
    file_item = await get_file(file_id)
    stored_path = resolve_path(Path(settings.storage_path), file_item.stored_name)
    if not stored_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stored file not found",
        )
    return file_item, stored_path
