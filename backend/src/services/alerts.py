from sqlalchemy import select
from src.db.models import Alert, StoredFile
from src.db.session import get_session


async def list_alerts() -> list[Alert]:
    result = await get_session().execute(select(Alert).order_by(Alert.created_at.desc()))
    return list(result.scalars().all())


def create_alert_for_file(file_item: StoredFile) -> Alert:
    if file_item.processing_status == "failed":
        level = "critical"
        message = "File processing failed"
    elif file_item.requires_attention:
        level = "warning"
        message = f"File requires attention: {file_item.scan_details}"
    else:
        level = "info"
        message = "File processed successfully"

    alert = Alert(file_id=file_item.id, level=level, message=message)
    get_session().add(alert)
    return alert
