# -*- coding: utf-8 -*-
import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv, find_dotenv
import requests

# 1. LOAD CONFIGURATION
# find_dotenv() must have () to work correctly
load_dotenv(find_dotenv())

db_password = os.getenv("DB_PASS")
SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SLACK_CHANNEL = "#audit-alerts"

# charset=utf8mb4 is essential for handling special characters
DB_CONN = f"mysql+pymysql://root:{db_password}@localhost:3306/sakila"
#DB_CONN = f"mysql+pymysql://root:{db_password}@localhost:3306/sakila?charset=utf8mb4"
engine = create_engine(DB_CONN)

report = []

# 2. SLACK UTILITY
def send_slack_notification(message):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}",
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "channel": SLACK_CHANNEL, 
        "text": message
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response_json = response.json()
        if response_json.get("ok"):
            print("🚀 Slack notification sent successfully!")
        else:
            print(f"❌ Slack Error: {response_json.get('error')}")
    except Exception as e:
        print(f"❌ Failed to connect to Slack: {e}")

# 3. AUDIT LOGIC
def find_all_duplicates():
    query = """
    SELECT a.*
    FROM mypayment a
    JOIN (
        SELECT payment_id, amount
        FROM mypayment
        GROUP BY payment_id, amount
        HAVING COUNT(*) > 1
    ) b ON a.payment_id = b.payment_id AND a.amount = b.amount
    ORDER BY a.payment_id;
    """

    print("🔎 Auditing the entire table (no LIMIT)...")
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            # result.keys() provides the column names for the DataFrame
            df_duplicates = pd.DataFrame(result.fetchall(), columns=result.keys())

        if not df_duplicates.empty:
            msg = f"⚠️ Found {len(df_duplicates)} duplicate records in total."
            print(msg)
            report.append(msg)
             
            # Export to CSV Log - Using a raw string (r"") for the Windows path
            csv_filename = r"C:\Users\ADMIN\My Drive\Python\exports\duplicate.csv"
            os.makedirs(os.path.dirname(csv_filename), exist_ok=True)
            
            df_duplicates.to_csv(csv_filename, index=False, mode="a", header=not os.path.exists(csv_filename))
            print(f"Success! Duplicate records exported to {csv_filename}.")
            
            # Send alert to Slack
            send_slack_notification(msg)

        else:
            print("✅ No duplicates found in the entire table.")
            
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    find_all_duplicates()