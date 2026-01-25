import sqlite3
import pandas as pd

# Connect to the database you created
conn = sqlite3.connect('titanic_simple.db')

# Write a SQL query
query = "SELECT * FROM raw_titanic_data WHERE Survived = 1 LIMIT 10"

# Read the result into a new DataFrame
df_survived = pd.read_sql_query(query, conn)

print(df_survived)

conn.close()

#SQLite is "serverless," meaning the database is just a single file on your hard drive