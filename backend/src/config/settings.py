"""Application settings loaded from environment variables."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.constants import APP_NAME, JWT_ALGORITHM_HS256


class Settings(BaseSettings):
    """Container for runtime configuration values."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    app_name: str = APP_NAME
    app_env: str = "dev"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@db:5432/auto_listings",
        alias="DATABASE_URL",
    )
    alembic_database_url: str | None = Field(default=None, alias="ALEMBIC_DATABASE_URL")

    jwt_secret: str = Field(default="change-me", alias="JWT_SECRET")
    jwt_algorithm: str = JWT_ALGORITHM_HS256
    jwt_exp_minutes: int = 60 * 24

    admin_username: str = Field(default="admin", alias="ADMIN_USERNAME")
    admin_password: str = Field(default="admin123", alias="ADMIN_PASSWORD")

    carsensor_api_url: str = Field(
        default="https://carsensor.net/api/listings", alias="CARSENSOR_API_URL"
    )
    scraper_interval_seconds: int = Field(default=600, alias="SCRAPER_INTERVAL_SECONDS")
    scraper_timeout_seconds: int = Field(default=20, alias="SCRAPER_TIMEOUT_SECONDS")
    scraper_retry_attempts: int = Field(default=3, alias="SCRAPER_RETRY_ATTEMPTS")
    redis_host: str = Field(default="redis", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")
    redis_db: int = Field(default=0, alias="REDIS_DB")

    telegram_bot_token: str = Field(default="", alias="TELEGRAM_BOT_TOKEN")
    llm_api_key: str = Field(default="", alias="LLM_API_KEY")
    llm_model: str = Field(default="gpt-4.1-mini", alias="LLM_MODEL")


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings.

    Returns:
        Loaded settings instance.
    """

    return Settings()
