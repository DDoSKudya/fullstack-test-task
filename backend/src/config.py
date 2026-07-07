from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/fileexchange"
    redis_url: str = "redis://redis:6379/0"
    storage_path: str = "/data/files"
    max_upload_bytes: int = 52_428_800
    log_level: str = "INFO"
    log_format: str = "console"
    docs_enabled: bool = True


settings = Settings()
