# SLACK intallation
from dotenv import load_dotenv, find_dotenv
import os
import requests

# Your Slack Bot Token and Channel
load_dotenv(find_dotenv()) # <--- Good practice to actually call the load function
SLACK_TOKEN = os.getenv('SLACK_TOKEN')
SLACK_CHANNEL = "#audit-alerts" 

def send_slack_notification(message):
    url = "https://slack.com/api/chat.postMessage"
    # Ensure token is in headers as a Bearer token
    headers = {
    "Authorization": f"Bearer {SLACK_TOKEN}",
    "Content-Type": "application/json; charset=utf-8" # Added charset
}
    data = {
        "channel": SLACK_CHANNEL, 
        "text": message
    }
    response = requests.post(url, headers=headers, json=data)
    print(f"Slack Response: {response.json()}")

   # ... your SLACK_TOKEN and function code ...

if __name__ == "__main__":
    # This only runs if you run SLACK.py directly
    send_slack_notification("Test message from SLACK.py main block")