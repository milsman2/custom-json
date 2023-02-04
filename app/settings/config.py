"""
Pydantic config and settings
"""
from dotenv import load_dotenv
from pydantic import BaseSettings
from typing import Optional
from enum import Enum
import os
from functools import lru_cache

load_dotenv()


class EnvironmentEnum(str, Enum):
    """
    Enumerate the application environments
    """

    PRODUCTION = "production"
    LOCAL = "local"


class GlobalConfig(BaseSettings):
    """
    Base configuration to be modified by specific environments
    """

    ENVIRONMENT: EnvironmentEnum
    DEBUG: bool = False
    TESTING: bool = False
    TIMEZONE: str = "America/Chicago"
    SLACK_WEBHOOK: str = os.environ.get("SLACK_WEBHOOK")

    class Config:
        """
        Define configuration as case sensitive
        """

        case_sensitive = True


class LocalConfig(GlobalConfig):
    """
    Local configurations
    """

    DEBUG: bool = True
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.LOCAL


class ProdConfig(GlobalConfig):
    """
    Production configurations
    """

    DEBUG: bool = False
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.PRODUCTION


class FactoryConfig:
    """
    Class creates a factory for configurations
    """

    def __init__(self, environment: Optional[str]):
        self.environment = environment

    def __call__(self) -> GlobalConfig:
        if self.environment == EnvironmentEnum.LOCAL.value:
            return LocalConfig()
        return ProdConfig()


@lru_cache()
def get_configuration() -> GlobalConfig:
    """
    Generate a configuration based on environment
    """
    return FactoryConfig(os.environ.get("ENVIRONMENT"))()


settings = get_configuration()
