import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv, find_dotenv
from SLACK import send_slack_notification

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
URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

# Local export config
EXPORT_DIR = r"C:\Python\export"
EXPORT_FILE = os.path.join(EXPORT_DIR, "raw_titanic_data.csv")


def run_titanic_pipeline():
    print("🚢 Starting Titanic Data Flow...")
    try:
        # 1. Extract
        df = pd.read_csv(URL)

        # 2. Transform (Simple cleanup)
        df.columns = [c.lower() for c in df.columns]  # lowercase columns

        # 3. Load to MySQL
        engine = create_engine(DB_CONN)
        df.to_sql("raw_titanic_data", engine, if_exists="replace", index=False)

        # 4. Save to local export folder (overwrite if exists)
        os.makedirs(EXPORT_DIR, exist_ok=True)
        df.to_csv(EXPORT_FILE, index=False)

        # Task 2 success message
        print(
            f"✅ Success! Loaded {len(df)} rows in export folder and Mysql as 'raw_titanic_data' table."
        )
       
        # Task 3 Slack success alert
        send_slack_notification(
            "✅ Success! load and save raw_titanic_data to MySQL and local Export folder."
        )

    except Exception as e:
        error_type = type(e).__name__
        error_message = f"❌ Titanic pipeline failed ({error_type}): {e}"
        print(error_message)

        # Task 3 Slack failure alert with detailed error type
        send_slack_notification(
            f"❌ failed - Titanic pipeline failed ({error_type}): {e}"
        )


if __name__ == "__main__":
    run_titanic_pipeline()