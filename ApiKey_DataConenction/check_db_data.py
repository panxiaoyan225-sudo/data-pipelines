import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

def verify_warehouse_data():
    # 1. Point to the same database file
    db_name = os.environ.get("DB_NAME", "practice_warehouse.db")
    connection = None
    
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        # 2. Execute a standard SQL SELECT statement
        # We'll fetch just the first 5 rows to verify the schema and contents
        print(f"🔍 Querying the 'staging_posts' table in {db_name}...")
        cursor.execute("SELECT id, userId, title FROM staging_posts LIMIT 5;")

        # 3. INTERVIEW HIGHLIGHT: Use fetchall() to retrieve the records from the cursor
        rows = cursor.fetchall()

        if not rows:
            print("⚠️ The table is empty! Run 'Python to SQL.py' first to ingest data.")
            return

        # 4. Loop through the rows to display the records
        print("\n🎯 Data Found inside SQLite Cursor:")
        print("-" * 60)
        for row in rows:
            # Each row comes back as a standard Python tuple
            print(f"Post ID: {row[0]} | User ID: {row[1]} | Title: {row[2][:40]}...")
        print("-" * 60)

        # 5. Get a quick total row count for data validation/auditing
        cursor.execute("SELECT COUNT(*) FROM staging_posts;")
        total_count = cursor.fetchone()[0] # fetchone() returns a 1-item tuple like (100,)
        print(f"📊 Total records successfully logged in table: {total_count}")

    except Exception as err:
        print(f"❌ Failed to read data from database: {err}")
        
    finally:
        # 6. Always clean up connections
        if connection:
            cursor.close()
            connection.close()
            print("\n🔌 Database verification connection closed.")

if __name__ == "__main__":
    verify_warehouse_data()