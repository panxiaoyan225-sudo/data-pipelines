import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv, find_dotenv
import os

from SLACK import send_slack_notification



# MySQL credentials
load_dotenv(find_dotenv())
user = os.getenv("DB_USER")
pw = os.getenv("DB_PASS")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db = os.getenv("DB_NAME")

DB_CONN = f"mysql+pymysql://{user}:{pw}@{host}:{port}/{db}?charset=utf8mb4"
URL = "http://universities.hipolabs.com/search?country=Canada"



df = pd.read_json(URL)
print("Columns in dataframe:", df.columns.tolist())


