import pandas as pd
import logging

# Set up professional logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_titanic_data(df):
    """
    Performs critical data quality checks for the Titanic dataset.
    Returns: (bool, list of errors)
    """
    errors = []
    
    # 1. Schema Check: Ensure all required columns exist
    required_cols = {'PassengerId', 'Survived', 'Pclass', 'Age', 'Fare'}
    if not required_cols.issubset(df.columns):
        errors.append(f"Missing columns: {required_cols - set(df.columns)}")

    # 2. Type Check: Age should be numeric
    if not pd.api.types.is_numeric_dtype(df['Age']):
        errors.append("Data Quality Issue: 'Age' column is not numeric.")

    # 3. Logic Check: Fare cannot be negative
    if (df['Fare'] < 0).any():
        negative_fares = df[df['Fare'] < 0].shape[0]
        errors.append(f"Validation Failure: Found {negative_fares} records with negative Fares.")

    # 4. Completeness Check: Survived should not have nulls
    if df['Survived'].isnull().any():
        errors.append("Integrity Error: Found null values in 'Survived' column.")

    if not errors:
        logging.info("✅ All Data Quality checks passed.")
        return True, []
    else:
        for error in errors:
            logging.error(f"❌ {error}")
        return False, errors

# --- Integration Logic ---
if __name__ == "__main__":
    # 1. Fetch data from a live source
    URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    logging.info(f"Fetching data from {URL}...")
    df = pd.read_csv(URL)

    # 2. Run the validation
    success, error_list = validate_titanic_data(df)

    # 3. Action based on validation result
    if success:
        logging.info("Validation successful. Proceeding to load data.")
        # load_to_mysql(df) # Ensure this function is defined elsewhere!
    else:
        logging.warning(f"Validation failed. {len(error_list)} issues found. Load aborted.")