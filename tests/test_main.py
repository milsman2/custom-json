"""Tests for notification payloads and CLI behavior."""

from datetime import datetime
from unittest.mock import Mock

import pytest
import requests

from custom_json.main import build_payload, send_notification


@pytest.fixture
def timestamp() -> datetime:
    return datetime(2026, 1, 2, 15, 4, 5)


@pytest.mark.parametrize(
    ("stage", "expected_title"),
    [
        ("build", "Build Completed"),
        ("deployment", "Build Deployed"),
        ("push", "Main branch merged"),
    ],
)
def test_build_payload_known_stage(
    stage: str, expected_title: str, timestamp: datetime
) -> None:
    payload = build_payload(stage, "Ada", timestamp)
    blocks = payload["blocks"]
    assert isinstance(blocks, list)
    assert blocks[0]["text"]["text"] == expected_title
    assert any("Ada" in str(block) for block in blocks)


def test_build_payload_unknown_stage(timestamp: datetime) -> None:
    payload = build_payload("unknown", None, timestamp)
    blocks = payload["blocks"]
    assert isinstance(blocks, list)
    assert "not recognized" in str(blocks[0])


def test_send_notification_posts_json(monkeypatch: pytest.MonkeyPatch) -> None:
    response = Mock()
    monkeypatch.setattr("custom_json.main.requests.post", Mock(return_value=response))
    send_notification("build", "Ada", "https://example.invalid/webhook")
    response.raise_for_status.assert_called_once()


def test_send_notification_propagates_http_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = Mock()
    response.raise_for_status.side_effect = requests.HTTPError("bad response")
    monkeypatch.setattr("custom_json.main.requests.post", Mock(return_value=response))
    with pytest.raises(requests.HTTPError):
        send_notification("build", None, "https://example.invalid/webhook")
