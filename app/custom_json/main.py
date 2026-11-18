"""Build and send Slack notifications for CI/CD lifecycle events."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
from loguru import logger

from custom_json.config import settings

WEBHOOK_TIMEOUT_SECONDS = 10


def build_payload(
    stage: str, author: str | None, timestamp: datetime
) -> dict[str, object]:
    """Create a Slack Block Kit payload for a lifecycle stage."""
    labels = {
        "build": ("Build Completed", "End Build Time"),
        "deployment": ("Build Deployed", "End Build Time"),
        "push": ("Main branch merged", "Merge Time"),
    }
    unknown_title = (
        f"Message type not recognized at {timestamp:%d/%m/%Y %I:%M:%S %p} :("
    )
    title, time_label = labels.get(stage, (unknown_title, ""))
    blocks: list[dict[str, object]] = [
        {"type": "header", "text": {"type": "plain_text", "text": title}},
    ]

    if stage in labels:
        fields: list[dict[str, str]] = [
            {
                "type": "mrkdwn",
                "text": f"*{time_label}*\n{timestamp:%d/%m/%Y %I:%M:%S %p}",
            },
        ]
        if author is not None:
            fields.append({"type": "mrkdwn", "text": f"*Author*: {author}"})
        blocks.extend(
            [
                {"type": "divider"},
                {"type": "section", "fields": fields},
                {"type": "divider"},
                {
                    "type": "section",
                    "fields": [{"type": "mrkdwn", "text": "Nice :heavy_check_mark:"}],
                },
            ]
        )

    return {"blocks": blocks}


def send_notification(stage: str, author: str | None, webhook_url: str) -> None:
    """Send a notification and raise an error for unsuccessful requests."""
    timestamp = datetime.now(ZoneInfo(settings.TIMEZONE))
    payload = build_payload(stage, author, timestamp)
    response = requests.post(
        webhook_url,
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
        timeout=WEBHOOK_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    logger.info("Sent '{}' notification to Slack", stage)


def create_parser() -> argparse.ArgumentParser:
    """Build the CLI parser, retaining the original capitalized option names."""
    parser = argparse.ArgumentParser(description="Send a Slack lifecycle notification.")
    parser.add_argument(
        "--Stage",
        "--stage",
        dest="stage",
        required=True,
        help="build, deployment, or push",
    )
    parser.add_argument(
        "--Author", "--author", dest="author", help="Notification author"
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""
    args = create_parser().parse_args(argv)
    if not settings.SLACK_WEBHOOK:
        logger.error("SLACK_WEBHOOK is not configured")
        return 2

    try:
        send_notification(args.stage, args.author, settings.SLACK_WEBHOOK)
    except requests.RequestException:
        logger.exception("Unable to send Slack notification")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
