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

# Integration Example:
# df = pd.read_csv('titanic.csv')
# success, _ = validate_titanic_data(df)
# if success:
#     load_to_mysql(df)