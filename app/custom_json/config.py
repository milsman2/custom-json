"""Application settings, loaded from environment variables or an optional .env file."""

from enum import Enum
from functools import lru_cache
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentEnum(str, Enum):
    """Supported runtime environments."""

    PRODUCTION = "production"
    LOCAL = "local"


class Settings(BaseSettings):
    """Validated application configuration."""

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.PRODUCTION
    DEBUG: bool = False
    TESTING: bool = False
    TIMEZONE: str = "America/Chicago"
    SLACK_WEBHOOK: str | None = Field(default=None, repr=False)

    @field_validator("TIMEZONE")
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        """Reject invalid IANA timezone names early."""
        try:
            ZoneInfo(value)
        except (ValueError, ZoneInfoNotFoundError) as exc:
            raise ValueError(f"Unknown timezone: {value}") from exc
        return value


GlobalConfig = Settings
LocalConfig = Settings
ProdConfig = Settings


class FactoryConfig:
    """Compatibility factory retained for existing imports."""

    def __init__(self, environment: str | None = None) -> None:
        self.environment = environment

    def __call__(self) -> Settings:
        environment = (
            EnvironmentEnum(self.environment)
            if self.environment is not None
            else EnvironmentEnum.PRODUCTION
        )
        return Settings(ENVIRONMENT=environment)


@lru_cache(maxsize=1)
def get_configuration() -> Settings:
    """Return the cached process-wide settings instance."""
    return Settings()


settings = get_configuration()

__all__ = [
    "EnvironmentEnum",
    "FactoryConfig",
    "GlobalConfig",
    "LocalConfig",
    "ProdConfig",
    "Settings",
    "get_configuration",
    "settings",
]
