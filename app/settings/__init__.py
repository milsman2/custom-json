"""Backward-compatible settings imports."""

try:
    from custom_json.config import settings
except ModuleNotFoundError:
    from app.custom_json.config import settings

__all__ = ["settings"]
