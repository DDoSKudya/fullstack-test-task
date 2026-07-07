from src.db.session import session_scope
from src.logging_config import configure_logging
from src.services.processing import run_pipeline
from src.worker.broker import broker

configure_logging()


@broker.task
async def process_file(file_id: str) -> None:
    async with session_scope():
        await run_pipeline(file_id)
