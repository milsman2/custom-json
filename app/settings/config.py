"""Backward-compatible re-exports of the settings API."""

try:
    from custom_json.config import (
        EnvironmentEnum,
        FactoryConfig,
        GlobalConfig,
        LocalConfig,
        ProdConfig,
        Settings,
        get_configuration,
        settings,
    )
except ModuleNotFoundError:
    from app.custom_json.config import (
        EnvironmentEnum,
        FactoryConfig,
        GlobalConfig,
        LocalConfig,
        ProdConfig,
        Settings,
        get_configuration,
        settings,
    )

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
