"""
All imports for sending a custom webhook
"""

import argparse
import json
from datetime import datetime

import pytz
import requests
from dotenv import load_dotenv
from icecream import ic
from settings.config import settings

load_dotenv()

now = datetime.now(pytz.timezone(settings.TIMEZONE)).strftime(
    "%d/%m/%Y %I:%M:%S %P"
)  # time object
parser = argparse.ArgumentParser()
parser.add_argument("--Stage", help="Stage")
parser.add_argument("--Author", help="Author")

args = parser.parse_args()

STAGE = args.Stage
AUTHOR = args.Author
SLACK_WEBHOOK = settings.SLACK_WEBHOOK


def main():
    """
    Different styling and input for each stage
    """
    ic()
    match STAGE:
        case "build":
            data = {
                "blocks": [
                    {
                        "type": "header",
                        "text": {"type": "plain_text", "text": "Build Completed"},
                    },
                    {"type": "divider"},
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": f"*End Build Time* \n{now}"},
                        ],
                    },
                    {
                        "type": "section",
                        "fields": [{"type": "mrkdwn", "text": f"*Author*: {AUTHOR}"}],
                    },
                    {"type": "divider"},
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": "Nice :heavy_check_mark:"}
                        ],
                    },
                ]
            }
        case "deployment":
            data = {
                "blocks": [
                    {
                        "type": "header",
                        "text": {"type": "plain_text", "text": "Build Deployed"},
                    },
                    {"type": "divider"},
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": f"*End Build Time* \n{now}"},
                        ],
                    },
                    {
                        "type": "section",
                        "fields": [{"type": "mrkdwn", "text": f"*Author*: {AUTHOR}"}],
                    },
                    {"type": "divider"},
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": "Nice :heavy_check_mark:"}
                        ],
                    },
                ]
            }
        case "push":
            data = {
                "blocks": [
                    {
                        "type": "header",
                        "text": {"type": "plain_text", "text": "Main branch merged"},
                    },
                    {"type": "divider"},
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": f"*Merge Time* \n{now}"},
                        ],
                    },
                    {
                        "type": "section",
                        "fields": [{"type": "mrkdwn", "text": f"*Author*: {AUTHOR}"}],
                    },
                    {"type": "divider"},
                    {
                        "type": "section",
                        "fields": [
                            {"type": "mrkdwn", "text": "Nice :heavy_check_mark:"}
                        ],
                    },
                ]
            }
        case _:
            data = {
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"Message type not recognized at {now} :(",
                        },
                    },
                ]
            }

    requests.post(
        SLACK_WEBHOOK,
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
        timeout=3,
    )


if __name__ == "__main__":
    ic()
    main()
