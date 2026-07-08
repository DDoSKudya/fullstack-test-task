import structlog
from sqlalchemy import select
from src.db.models import Alert, StoredFile
from src.db.session import get_session

logger = structlog.get_logger()


async def list_alerts(limit: int = 50, offset: int = 0) -> list[Alert]:
    result = await get_session().execute(
        select(Alert).order_by(Alert.created_at.desc()).limit(limit).offset(offset)
    )
    return list(result.scalars())


def create_alert_for_file(file_item: StoredFile) -> None:
    if file_item.processing_status == "failed":
        level = "critical"
        message = "File processing failed"
    elif file_item.requires_attention:
        level = "warning"
        message = f"File requires attention: {file_item.scan_details}"
    else:
        level = "info"
        message = "File processed successfully"

    get_session().add(Alert(file_id=file_item.id, level=level, message=message))
    logger.info("alert.created", file_id=file_item.id, level=level)
