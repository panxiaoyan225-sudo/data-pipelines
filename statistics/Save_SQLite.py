import pandas as pd
import sqlite3

def extract_and_load_raw():
    # 1. Extract: Download the Titanic dataset
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    
    try:
        print("--- START: Downloading data ---")
        df = pd.read_csv(url)
        print("--- SUCCESS: Data downloaded ---")

        # 2. Connection: Use built-in sqlite3 (No SQLAlchemy needed)
        # This creates a file named 'titanic_simple.db' in your current folder
        conn = sqlite3.connect('titanic_simple.db')

        # 3. Load: Push it into the SQLite database
        print("--- START: Loading into SQLite ---")
        df.to_sql('raw_titanic_data', conn, if_exists='replace', index=False)
        
        # Show descriptive information of the database
        print("\nDescriptive information of the database:")
        # Create a cursor object which allows us to execute SQL commands on the SQLite database.
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info('raw_titanic_data')")
        columns_info = cursor.fetchall()
        for col in columns_info:
            print(f"Column: {col[1]}, Type: {col[2]}")
        cursor.close()
        
        # Close the connection
        conn.close()
            
        print("--- SUCCESS: Data loaded into local SQLite (titanic_simple.db) ---")
        print("\nPreview of loaded data:")
        print(df.head())
       # This shows counts, unique values, top values, and frequencies for strings 
# alongside the mean, std, and quartiles for numbers.
       # 1. Force pandas to show all columns regardless of how many there are
        pd.set_option('display.max_columns', None)

# 2. Force pandas to expand the width of the display so it doesn't wrap
        pd.set_option('display.width', 1000)

# Now when you run this, it will show everything:
        print(df.describe(include='all'))
       
        
    # The following except block is triggered if any error occurs in the try block above. 
    # It catches all exceptions and assigns the exception object to the variable 'e'.
    #Without as e, you know an error happened, but you don't know what it was. With it, you can get specific
    except Exception as e:
        print(f"--- FAILURE: {e}")

if __name__ == "__main__":
    extract_and_load_raw()