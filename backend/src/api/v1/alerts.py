from typing import Annotated

from fastapi import APIRouter, Query
from src.api.schemas import AlertItem
from src.db.models import Alert
from src.services import alerts as alerts_service

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertItem])
async def list_alerts(
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[Alert]:
    return await alerts_service.list_alerts(limit, offset)
