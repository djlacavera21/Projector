from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the Projector API."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    environment: str = Field(default="development", alias="PROJECTOR_ENV")
    database_url: str = Field(default="sqlite+aiosqlite:///./projector.db", alias="DATABASE_URL")
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    s3_endpoint: str = Field(default="http://localhost:9000", alias="S3_ENDPOINT")
    s3_bucket: str = Field(default="projector-media", alias="S3_BUCKET")
    jwt_secret: str = Field(default="change-me-before-production", alias="JWT_SECRET")


settings = Settings()
