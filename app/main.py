"""
All imports for sending a custom webhook
"""
import os
import json
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()
now = datetime.now().time() # time object

SLACK_WEBHOOK = os.environ.get('SLACK_WEBHOOK')
AUTHOR = os.environ.get('AUTHOR')
STAGE = os.environ.get('STAGE')

match STAGE:
    case 'build':
        data = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Build Completed"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*End Build Time* \n{now} UTC"
                        },
                    ]
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*Author*"
                        }
                    ]
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "Nice :heavy_check_mark:"
                        }
                    ]
                },
            ]
        }
    case 'push':
        data = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Main branch merged"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Merge Time* \n{now} UTC"
                        },
                    ]
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*Author*"
                        }
                    ]
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "Nice :heavy_check_mark:"
                        }
                    ]
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
                        "text": "Message type not recognized :("
                    }
                },
            ]
        }

requests.post(SLACK_WEBHOOK, data=json.dumps(data), headers={'Content-Type': 'application/json'}, timeout=3)
