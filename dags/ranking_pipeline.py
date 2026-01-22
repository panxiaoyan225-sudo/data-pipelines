import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

db_password = os.getenv("DB_PASS")

# Configuration
DB_CONN = f"mysql+pymysql://root:{db_password}@localhost:3306/sakila"
# Public API for university data
URL = "http://universities.hipolabs.com/search?country=Canada"

def run_ranking_pipeline():
    print("🎓 Starting University Ranking Pipeline...")
    
    # 1. Extract
    df = pd.read_json(URL)
    
    # --- OPTION A: Clean BEFORE Renaming (Recommended) ---
# 2. Transform
    df = df[['name', 'state-province', 'domains', 'web_pages']]

# Clean the lists using the ORIGINAL names from the JSON
    df['domains'] = df['domains'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
    df['web_pages'] = df['web_pages'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

# NOW rename them for MySQL
    df.columns = ['univ_name', 'province', 'domain', 'website']

    
    # 3. Load
    engine = create_engine(DB_CONN)
    df.to_sql('raw_university_data', engine, if_exists='replace', index=False)
    
    print(f"✅ Success! Loaded {len(df)} Canadian universities into MySQL.")

if __name__ == "__main__":
    run_ranking_pipeline()