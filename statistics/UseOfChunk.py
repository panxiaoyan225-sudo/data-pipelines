
import pandas as pd
from sqlalchemy import create_engine

from dotenv import load_dotenv, find_dotenv
import os
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
# Using your credentials
engine = create_engine(DB_CONN)


def audit_by_chunks():
    print("🟢 Step 1: Script started...") # The script has started
    chunk_size = 50000
    all_duplicates = []
    
    # Use a basic SELECT to test
    query = "SELECT * FROM mypayment"
    print(f"🟡 Step 2: Connecting to database to run: {query}")
    
    # The 'chunk' here is a pandas DataFrame representing a subset of rows read from the database.
    # Using 'chunksize' reads the data in portions instead of all at once, preventing memory overload for large tables.
    for i, chunk in enumerate(pd.read_sql(query, engine, chunksize=chunk_size)):
        print(f"📦 Step 3: Processing Chunk #{i+1}... (Chunk shape: {chunk.shape})")
        # We process each 'chunk' independently to check for duplicates within this portion.
        # 'chunk' enables us to efficiently handle large datasets piece by piece.
        dupes = chunk[chunk.duplicated(subset=['payment_id', 'amount'], keep=False)]
        #if statement in the code is used for printing a warning message, not for deciding whether or not to store the data
        if not dupes.empty:
            print(f"⚠️ Found {len(dupes)} duplicates in this chunk!")

        all_duplicates.append(dupes)

if __name__ == "__main__":
    audit_by_chunks()