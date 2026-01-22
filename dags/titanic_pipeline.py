import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

db_password = os.getenv("DB_PASS")
# Configuration
DB_CONN = f"mysql+pymysql://root:{db_password}@localhost:3306/sakila"
URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

def run_titanic_pipeline():
    print("🚢 Starting Titanic Data Flow...")
    
    # 1. Extract
    df = pd.read_csv(URL)
    
    # 2. Transform (Simple cleanup)
    df.columns = [c.lower() for c in df.columns] # lowercase columns
    
    # 3. Load
    engine = create_engine(DB_CONN)
    df.to_sql('raw_titanic_data', engine, if_exists='replace', index=False)
    
    print(f"✅ Success! Loaded {len(df)} rows into 'raw_titanic_data' table.")

if __name__ == "__main__":
    run_titanic_pipeline()