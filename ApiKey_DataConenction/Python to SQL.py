import os
import sqlite3
from dotenv import load_dotenv

# 1. IMPORT YOUR API PIPELINE FUNCTION
# Since 'api_pipeline.py' is in the same 'workflow' folder, you can import it directly:
from api_pipeline import get_api_data

load_dotenv()

def ingest_data_to_db(data_records):
    # Ensure there is data to process
    if not data_records:
        print("⚠️ No data records provided for ingestion. Skipping step.")
        return

    # Create target schema matching your JSON fields
    # (Included 'userId' to capture the complete JSONPlaceholder schema)
    db_name = os.environ.get("DB_NAME", "practice_warehouse.db")
    connection = None
    
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        # 2. Create target schema
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS staging_posts (
                id INTEGER PRIMARY KEY,
                userId INTEGER,
                title TEXT,
                body TEXT
            )
        """)

        # 3. Parameterized query to prevent SQL Injection
        insert_query = "INSERT OR REPLACE INTO staging_posts (id, userId, title, body) VALUES (?, ?, ?, ?)"
        
        # Parse out the dynamic dictionary keys safely using .get()
        batch_data = [
            (item.get('id'), item.get('userId'), item.get('title'), item.get('body')) 
            for item in data_records
        ]
        
        cursor.executemany(insert_query, batch_data)
        
        # 4. Commit transactions explicitly
        connection.commit()
        print(f"✅ Database Ingestion Complete. {cursor.rowcount} rows merged into '{db_name}'.")

    except Exception as db_err:
        if connection:
            connection.rollback()  
        print(f"❌ Database transaction failed: {db_err}")
    
    finally:
        # 5. ALWAYS close database connections to prevent leaks
        if connection:
            cursor.close()
            connection.close()
            print("🔌 Database connection closed cleanly.")



# 6. RUN THE END-TO-END PIPELINE
if __name__ == "__main__":
    print("🚀 Starting End-to-End Workflow Pipeline...")
    
    # 📍 THIS IS WHERE THE DATA COMES IN:
    # This line runs the function from your first script and saves the result here.
    api_payload = get_api_data()   
    
    # If you want to SEE the raw data in your console before it goes to SQL, 
    # you can add a print statement right here:
    print("👀 Raw data fetched from API:", api_payload[:2]) # Prints just the first 2 records
    
    # 📍 THIS IS WHERE THE DATA IS HANDLED:
    # We take that 'api_payload' variable and pass it directly into your database function.
    if api_payload:
        ingest_data_to_db(api_payload) 
    else:
        print("❌ Pipeline halted: Failed to extract data from the API.")