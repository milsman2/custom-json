"""
All imports for sending a custom webhook
"""
import json
from datetime import datetime
import argparse
import requests
from dotenv import load_dotenv

load_dotenv()
now = datetime.now().time()  # time object
parser = argparse.ArgumentParser()
parser.add_argument("--Stage", help = "Stage")
parser.add_argument("--Author", help = "Author")
parser.add_argument("--Webhook",  help = "Slack Webhook")

args = parser.parse_args()

STAGE = args.Stage
AUTHOR = args.Author
SLACK_WEBHOOK = args.Webhook

def main():
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
                            {"type": "mrkdwn", "text": f"*End Build Time* \n{now} UTC"},
                        ],
                    },
                    {"type": "section", "fields": [{"type": "mrkdwn", "text": f"*Author*: {AUTHOR}"}]},
                    {"type": "divider"},
                    {
                        "type": "section",
                        "fields": [{"type": "mrkdwn", "text": "Nice :heavy_check_mark:"}],
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
                            {"type": "mrkdwn", "text": f"*End Build Time* \n{now} UTC"},
                        ],
                    },
                    {"type": "section", "fields": [{"type": "mrkdwn", "text": f"*Author*: {AUTHOR}"}]},
                    {"type": "divider"},
                    {
                        "type": "section",
                        "fields": [{"type": "mrkdwn", "text": "Nice :heavy_check_mark:"}],
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
                            {"type": "mrkdwn", "text": f"*Merge Time* \n{now} UTC"},
                        ],
                    },
                    {"type": "section", "fields": [{"type": "mrkdwn", "text": f"*Author*: {AUTHOR}"}]},
                    {"type": "divider"},
                    {
                        "type": "section",
                        "fields": [{"type": "mrkdwn", "text": "Nice :heavy_check_mark:"}],
                    },
                ]
            }
        case default:
            data = {
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Message type not recognized :(",
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
    main()
