from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/fileexchange"
    redis_url: str = "redis://redis:6379/0"
    storage_path: str = "/data/files"
    max_upload_mb: int = 50
    scan_max_mb: int = 10
    log_level: str = "INFO"
    log_format: str = "console"
    docs_enabled: bool = True
    testing: bool = False

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_mb * 1024 * 1024

    @property
    def scan_max_bytes(self) -> int:
        return self.scan_max_mb * 1024 * 1024


settings = Settings()
