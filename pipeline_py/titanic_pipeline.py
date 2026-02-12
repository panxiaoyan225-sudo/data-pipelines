import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv, find_dotenv
import os

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

def run_titanic_pipeline():
    print("🚢 Starting Titanic Data Flow...")
    try:
        # 1. Extract
        df = pd.read_csv(URL)
        
        # 2. Transform (Simple cleanup)
        df.columns = [c.lower() for c in df.columns] # lowercase columns
        
        # 3. Load
        engine = create_engine(DB_CONN)
        df.to_sql('raw_titanic_data', engine, if_exists='replace', index=False)
        
        print(f"✅ Success! Loaded {len(df)} rows into 'raw_titanic_data' table.")
    except Exception as e:
        print(f"❌ Titanic pipeline failed: {e}")

if __name__ == "__main__":
    run_titanic_pipeline()