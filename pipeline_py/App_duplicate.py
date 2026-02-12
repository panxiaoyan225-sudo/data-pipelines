# identify duplicate records by payment_id, you can use the Pandas .duplicated() method. 
#This is a very efficient way to flag data quality issues in a data & analytics workflow.
import pandas as pd
from sqlalchemy import create_engine

def get_db_connection(user, password, host, port, database):
    conn_str = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    # The following line initializes and returns an SQLAlchemy Engine, which serves as the primary interface
    # for connecting to and working with a SQL database (in this case, a MySQL database using pymysql).
    # The `conn_str` includes the username, password, host, port, and database name, allowing SQLAlchemy
    # to know how to establish the database connection.
    return create_engine(conn_str)

def run_duplicate_check(engine, table, id_column):
    print("🔎 Starting Duplicate Check...")

    try:
        # Read data
        df = pd.read_sql(f"SELECT * FROM {table} LIMIT 10000", engine)

        if id_column not in df.columns:
            print(f"❌ ERROR: {id_column} does not exist in table {table}.")
            return

        duplicate_mask = df.duplicated(subset=[id_column], keep=False)
        # multi_duplicate_mask = df.duplicated(subset=['payment_id', 'amount'], keep=False)
        # Identifying 100% identical clones
        # Since subset is NOT used, it checks every column automatically
        #duplicate_clones = df[df.duplicated(keep=False)]

        wrong_records = df[duplicate_mask].sort_values(by=id_column)
        
        # Check if the DataFrame 'wrong_records' is not empty,
        # meaning duplicate records have been detected in the data.
        if not wrong_records.empty:
            num_errors = len(wrong_records)
            unique_ids = wrong_records[id_column].nunique()
            
            print(f"⚠️ ERROR: Found {num_errors} duplicate records affecting {unique_ids} unique {id_column}s!")
            print("-" * 30)
            print(wrong_records.head(20))  # Show only up to 20 records for clarity
            print("-" * 30)
        else:
            print(f"✅ No duplicate {id_column} found in {table}.")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("Welcome to the Duplicate Record Checker!")
    user = input("Enter MySQL username: ")
    password = input("Enter MySQL password: ")
    host = input("Enter host [default: localhost]: ") or "localhost"
    port = input("Enter port [default: 3306]: ") or "3306"
    database = input("Enter database name: ")
    table = input("Enter table name: ")
    id_column = input("Enter the column name to check for duplicates (e.g. payment_id): ")
    
    engine = get_db_connection(user, password, host, port, database)
    run_duplicate_check(engine, table, id_column)

if __name__ == "__main__":
    main()