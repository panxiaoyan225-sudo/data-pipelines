import pandas as pd
import logging
import os
import pymysql
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up professional logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def validate_titanic_data(df):
    """
    Performs critical data quality checks for the Titanic dataset.
    Returns: (bool, list of errors)
    """
    errors = []
    
    try:
        # 1. Schema Check: Ensure all required columns exist
        required_cols = {'PassengerId', 'Survived', 'Pclass', 'Age', 'Fare'}
        if not required_cols.issubset(df.columns):
            missing = required_cols - set(df.columns)
            errors.append(f"Missing columns: {missing}")

        # 2. Type Check: Age should be numeric
        if 'Age' in df.columns and not pd.api.types.is_numeric_dtype(df['Age']):
            errors.append("Data Quality Issue: 'Age' column is not numeric.")

        # 3. Logic Check: Fare cannot be negative
        if 'Fare' in df.columns and (df['Fare'] < 0).any():
            negative_count = df[df['Fare'] < 0].shape[0]
            errors.append(f"Validation Failure: Found {negative_count} records with negative Fares.")

        # 4. Completeness Check: Survived should not have nulls
        if 'Survived' in df.columns and df['Survived'].isnull().any():
            errors.append("Integrity Error: Found null values in 'Survived' column.")

    except Exception as e:
        logging.error(f"Unexpected error during validation: {e}")
        return False, [str(e)]

    if not errors:
        logging.info("✅ All Data Quality checks passed.")
        return True, []
    else:
        for error in errors:
            logging.error(f"❌ {error}")
        return False, errors

def load_to_mysql(df, table_name="titanic_records"):
    """
    Creates the database if it doesn't exist and loads the DataFrame to MySQL.
    """
    # Fetching all components from .env
    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    port = os.getenv("DB_PORT", "3306")
    db_name = "titanic_db"

    try:
        # 1. Connect to MySQL server (without DB) to ensure the DB exists
        conn = pymysql.connect(
            host=host,
            user=user,
            password=db_pass,
            port=int(port)
        )
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        conn.commit()
        conn.close()

        # 2. Create SQLAlchemy engine to specific database
        connection_uri = f"mysql+pymysql://{user}:{db_pass}@{host}:{port}/{db_name}?charset=utf8mb4"
        engine = create_engine(connection_uri)

        # 3. Load data
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        logging.info(f"🚀 Successfully loaded {len(df)} rows into {table_name}.")

    except Exception as e:
        logging.error(f"Failed to load data to MySQL: {e}")

# --- Execution Block ---
if __name__ == "__main__":
    # 1. Fetch data
    URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    logging.info("Fetching data from source...")
    
    try:
        titanic_df = pd.read_csv(URL)
        
        # 2. Validate data
        success, errors = validate_titanic_data(titanic_df)
        
        # 3. Load data only if validation passes
        if success:
            load_to_mysql(titanic_df)
        else:
            logging.warning(f"Data load aborted. {len(errors)} validation errors found.")
            
    except Exception as e:
        logging.critical(f"Pipeline failed: {e}")