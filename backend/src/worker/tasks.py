import time

import structlog
from src.db.session import session_scope
from src.logging_config import configure_logging
from src.services.processing import run_pipeline
from src.worker.broker import broker

configure_logging()
logger = structlog.get_logger()


@broker.task
async def process_file(file_id: str) -> None:
    structlog.contextvars.bind_contextvars(file_id=file_id)
    started = time.perf_counter()
    logger.info("task.started")
    try:
        async with session_scope():
            status = await run_pipeline(file_id)
    except Exception as exc:
        logger.exception("task.failed", error_type=type(exc).__name__)
        raise
    duration_ms = round((time.perf_counter() - started) * 1000, 2)
    logger.info("task.completed", duration_ms=duration_ms, processing_status=status)
