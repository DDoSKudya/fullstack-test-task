from fastapi import FastAPI
from src.config import settings
from src.logging_config import configure_logging

configure_logging()

app = FastAPI(
    title="File Exchange API",
    docs_url="/docs" if settings.docs_enabled else None,
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
async def ready() -> dict[str, str]:
    return {"status": "ready"}
