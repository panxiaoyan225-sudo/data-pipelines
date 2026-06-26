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
        # The 'response' object captures the HTTP response from Slack's API after sending the POST request.
        # It contains status info (like 200 OK), payload data, and error details if any.
        response = requests.post(url, headers=headers, json=data, timeout=10)
        # Status info example:
        #   response.status_code == 200  # OK: request succeeded
        #   response.status_code == 400  # Bad Request
        #   response.status_code == 401  # Unauthorized
        #   response.status_code == 403  # Forbidden
        #   response.status_code == 404  # Not Found
        #   response.status_code == 429  # Too Many Requests (Rate limiting)
        #   response.status_code == 500  # Internal Server Error (Slack problem)
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