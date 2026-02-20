import pandas as pd
from sqlalchemy import create_engine
import pymysql
from datetime import datetime
import requests
from dotenv import load_dotenv, find_dotenv
import os
import sys
# Add the directory containing the file to the system path
sys.path.append(r'C:\Python\Basic\codes')
# Now you can import the file name (without the .py extension)
from SLACK import send_slack_notification

# 1. CONFIGURATION
# MySQL credentials
load_dotenv(find_dotenv())
# Fetching all components from .env
user = os.getenv("DB_USER")
pw = os.getenv("DB_PASS")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db = os.getenv("DB_NAME")

# A cleaner, more professional connection string
DB_CONN = f"mysql+pymysql://{user}:{pw}@{host}:{port}/{db}?charset=utf8mb4"



def run_audit():
    try:
        engine = create_engine(DB_CONN)
        df = pd.read_sql("SELECT * FROM payment", engine)
        
        # 'report' is a list used to collect audit issue messages identified during the data audit,
        # so they can be printed and also sent as a summary (if any issues are found) to Slack.
        report = []
        print(f"\n--- Starting Audit: {datetime.now().strftime('%Y-%m-%d %H:%M')} ---")

        # 2. AUDIT: DUPLICATES
        # This line checks for duplicate records in the DataFrame based on the 'payment_id' column.
        # The pandas .duplicated('payment_id', keep=False) method returns a boolean Series that is True 
        # for all rows that have the same value in 'payment_id' as another row (including all duplicates, not just the second occurrence).
        # By using df[ ... ], we filter the original DataFrame to only those rows where 'payment_id' is duplicated.
        
        # The resulting 'duplicates' DataFrame will contain every row involved in a duplicate 'payment_id', 
        # which can then be summarized, reported, or further analyzed.
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




if __name__ == "__main__":
    run_audit()
    send_slack_notification("✅  audit check completed.")
