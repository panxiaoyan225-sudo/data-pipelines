# SLACK.py (tiny hardening patch)
from dotenv import load_dotenv, find_dotenv
import os
import requests

load_dotenv(find_dotenv())
SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SLACK_CHANNEL = "#audit-alerts"


def send_slack_notification(message):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}",
        "Content-Type": "application/json; charset=utf-8",
    }
    data = {"channel": SLACK_CHANNEL, "text": message}

    try:
        # timeout added to avoid hanging forever
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()  # HTTP-level errors (4xx/5xx)

        payload = response.json()
        # Slack API-level error check (ok:false)
        if not payload.get("ok", False):
            print(f"Slack API error: {payload.get('error', 'unknown_error')}")
            return False

        return True

    except requests.RequestException as e:
        print(f"Slack request failed: {e}")
        return False