# -*- coding: utf-8 -*-
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv, find_dotenv
import requests

# 1. LOAD CONFIGURATION
# find_dotenv() must have () to work correctly
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
#DB_CONN = f"mysql+pymysql://root:{db_password}@localhost:3306/sakila?charset=utf8mb4"
engine = create_engine(DB_CONN)

# Get base path from .env
# If EXPORT_PATH is missing, it defaults to the current directory ('.')
base_path = os.getenv("EXPORT_PATH", ".")
# 2. Combine the path with the filename
# This creates: C:\Users\ADMIN\My Drive\Python\exports\duplicate.csv
csv_filename = os.path.join(base_path, "duplicate.csv")
# 3. Ensure the folder exists (important if you move to a new computer)
os.makedirs(os.path.dirname(csv_filename), exist_ok=True)

SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SLACK_CHANNEL = "#audit-alerts"
report = []
# 2. SLACK UTILITY
# Import send_slack_notification from SLACK.py instead of redefining it
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from SLACK import send_slack_notification
   

# 3. AUDIT LOGIC
def find_all_duplicates():
    print("[AUDIT] Auditing the entire table (no LIMIT)...")

    try:
        with engine.connect() as conn:
            df = pd.read_sql("SELECT * FROM mypayment", conn)

        dup_mask = df.duplicated(subset=["payment_id", "amount"], keep=False)
        df_duplicates = df[dup_mask].sort_values("payment_id")

        if not df_duplicates.empty:
            msg = f"⚠️ Found {len(df_duplicates)} duplicate records in total."
            print(msg)
            report.append(msg)
             
            # Export to CSV Log - Using a raw string (r"") for the Windows path
            #csv_filename = r"C:\Users\ADMIN\My Drive\Python\exports\duplicate.csv"
         

            df_duplicates.to_csv(csv_filename, index=False, mode="a", header=not os.path.exists(csv_filename))
            print(f"Success!  {len(df_duplicates)}  Duplicate records exported to {csv_filename}.")
            
            # Send alert to Slack
            send_slack_notification(msg)

        else:
            print("✅ No duplicates found in the entire table.")
            
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    find_all_duplicates()