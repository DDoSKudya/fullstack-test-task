from fastapi import APIRouter
from src.api.schemas import AlertItem
from src.db.models import Alert
from src.services import alerts as alerts_service

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertItem])
async def list_alerts() -> list[Alert]:
    return await alerts_service.list_alerts()
