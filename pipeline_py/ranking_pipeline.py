import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv, find_dotenv
import os
import logging
import sys

# 1. Setup Logging to both Console and File
log_filename = "pipeline.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename, mode='w'), # 'w' replaces the file every run
        logging.StreamHandler(sys.stdout)           # Still shows in GCP Logs Explorer
    ]
)
logger = logging.getLogger(__name__)

# MySQL credentials
load_dotenv(find_dotenv())
user = os.getenv("DB_USER")
pw = os.getenv("DB_PASS")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db = os.getenv("DB_NAME")

DB_CONN = f"mysql+pymysql://{user}:{pw}@{host}:{port}/{db}?charset=utf8mb4"
URL = "http://universities.hipolabs.com/search?country=Canada"

def run_ranking_pipeline():
    logger.info("🎓 Starting University Ranking Pipeline...")
    
    try:
        # 1. Extract
        logger.info(f"Downloading data from {URL}...")
        df = pd.read_json(URL)
        
        # 2. Transform
        df = df[['name', 'state-province', 'domains', 'web_pages']]
        df['domains'] = df['domains'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
        df['web_pages'] = df['web_pages'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
        df.columns = ['univ_name', 'province', 'domain', 'website']
        
        # 3. Save CSV to root folder (overwrites if exists)
        csv_filename = "university_rankings.csv"
        df.to_csv(csv_filename, index=False)
        logger.info(f"💾 CSV saved locally as {csv_filename}")
        
        # 4. Load to MySQL
        engine = create_engine(DB_CONN)
        df.to_sql('raw_university_data', engine, if_exists='replace', index=False)
        
        logger.info(f"✅ Success! Loaded {len(df)} universities into MySQL.")

    except Exception as e:
        logger.error(f"❌ Pipeline Failed: {str(e)}")
        raise

if __name__ == "__main__":
    run_ranking_pipeline()