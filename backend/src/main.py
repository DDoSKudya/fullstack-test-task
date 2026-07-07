from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from src.api.middleware.db_session import db_session_middleware
from src.api.middleware.http_logging import http_logging_middleware
from src.api.middleware.request_id import request_id_middleware
from src.api.v1 import alerts, files
from src.config import settings
from src.db.session import get_session
from src.logging_config import configure_logging

configure_logging()

app = FastAPI(
    title="File Exchange API",
    docs_url="/docs" if settings.docs_enabled else None,
)
app.middleware("http")(http_logging_middleware)
app.middleware("http")(request_id_middleware)
app.middleware("http")(db_session_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(files.router, prefix="/api/v1")
app.include_router(alerts.router, prefix="/api/v1")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready", response_model=None)
async def ready() -> JSONResponse | dict[str, str]:
    try:
        await get_session().execute(text("SELECT 1"))
    except Exception:
        return JSONResponse(
            status_code=503,
            content={"status": "not ready", "database": "error"},
        )
    return {"status": "ready", "database": "ok"}
