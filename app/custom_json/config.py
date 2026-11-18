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


class GlobalConfig(BaseSettings):
    """Base configuration shared by all runtime environments."""

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


class LocalConfig(GlobalConfig):
    """Settings for local development."""

    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.LOCAL
    DEBUG: bool = True


class ProdConfig(GlobalConfig):
    """Settings for production deployments."""

    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.PRODUCTION
    DEBUG: bool = False


# Modern name retained alongside the original configuration class names.
Settings = GlobalConfig


class FactoryConfig:
    """Create the appropriate settings class for an environment."""

    def __init__(self, environment: str | None = None) -> None:
        """Store the environment name used to select a settings class."""
        self.environment = environment

    def __call__(self) -> GlobalConfig:
        """Instantiate local settings only for the local environment."""
        if self.environment == EnvironmentEnum.LOCAL.value:
            return LocalConfig()
        return ProdConfig()


@lru_cache(maxsize=1)
def get_configuration() -> GlobalConfig:
    """Return the cached process-wide settings instance."""
    import os

    return FactoryConfig(os.getenv("ENVIRONMENT"))()


settings = get_configuration()
app_settings = settings

__all__ = [
    "EnvironmentEnum",
    "FactoryConfig",
    "GlobalConfig",
    "LocalConfig",
    "ProdConfig",
    "Settings",
    "app_settings",
    "get_configuration",
    "settings",
]
