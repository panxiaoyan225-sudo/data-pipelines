import pandas as pd
from sqlalchemy import create_engine
import pymysql
from datetime import datetime
import requests
from dotenv import load_dotenv, find_dotenv
import os
# 1. CONFIGURATION
# MySQL credentials
load_dotenv(find_dotenv())
db_password = os.getenv('DB_PASS')
DB_CONN = f"mysql+pymysql://root:{db_password}@localhost:3306/sakila"

# Your Slack Bot Token and Channel

SLACK_TOKEN = os.getenv('SLACK_TOKEN')
SLACK_CHANNEL = "#audit-alerts" 



def run_audit():
    try:
        engine = create_engine(DB_CONN)
        df = pd.read_sql("SELECT * FROM payment", engine)
        
        # 'report' is a list used to collect audit issue messages identified during the data audit,
        # so they can be printed and also sent as a summary (if any issues are found) to Slack.
        report = []
        print(f"\n--- Starting Audit: {datetime.now().strftime('%Y-%m-%d %H:%M')} ---")

        # 2. AUDIT: DUPLICATES
        duplicates = df[df.duplicated('payment_id', keep=False)]
        if not duplicates.empty:
            msg = f"❌ CRITICAL: Found {len(duplicates)} duplicate payment IDs!"
            report.append(msg)
            print(msg)

        # 3. AUDIT: IMPOSSIBLE DATA
        impossible = df[df['amount'] > 10]
        if not impossible.empty:
            msg = f"⚠️ WARNING: Found {len(impossible)} payments > $10."
            report.append(msg)
            print(msg)

        # 4. SEND ALERT IF ISSUES FOUND
        if report:
            full_message = f"*Audit Report Found Issues:*\n" + "\n".join(report)
            send_slack_notification(full_message)
        else:
            print("✅ Check Passed: No issues found.")

        print("--- Audit Complete ---\n")

    except Exception as e:
        error_msg = f"🚨 Pipeline Failed: {str(e)}"
        print(error_msg)
        send_slack_notification(error_msg)

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


if __name__ == "__main__":
    run_audit()
    send_slack_notification("✅  audit check completed.")
