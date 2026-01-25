from airflow import DAG  # Airflow DAG is the core object for scheduling workflows
from airflow.operators.python import PythonOperator  # Operator to run Python functions as tasks
from airflow.operators.bash import BashOperator  # Operator to run Bash commands as tasks
from datetime import datetime  # Used for setting scheduling times
import pandas as pd  # For data manipulation and reading CSV files
from sqlalchemy import create_engine  # Allows Python to interact with SQL databases

def ingest_ranking_data():
    # Download university rankings CSV from GitHub
    url = "https://raw.githubusercontent.com/nogibjj/IDS-Week7_MiniProject_us26/main/World%20University%20Rankings%202023.csv"
    df = pd.read_csv(url)  # Load the CSV into a pandas DataFrame
    
    # Create a connection to the Postgres database inside Docker.
    # 'postgres' is the hostname of the database inside the Docker network.
    engine = create_engine('postgresql://airflow:airflow@postgres:5432/airflow')
    
    # Write the DataFrame to a new SQL table. Replace the table if it already exists.
    df.to_sql('raw_university_ranking', engine, if_exists='replace', index=False)

# Define an Airflow DAG (Directed Acyclic Graph) to orchestrate workflow
with DAG(
    'university_ranking_pipeline',  # Unique identifier for this pipeline
    start_date=datetime(2024, 1, 1),  # When to start scheduling the DAG
    schedule='@daily',  # Run the pipeline once per day
    catchup=False  # Only run from current day onward, do not backfill
) as dag:

    # Task 1: Run Python function to ingest the university ranking data
    task_ingest = PythonOperator(
        task_id='ingest_ranking_data',  # Unique task name
        python_callable=ingest_ranking_data  # Which function to execute
    )

    # Task 2: Run a Bash command to invoke dbt for data transformation
    task_transform = BashOperator(
        task_id='run_dbt_ranking',  # Unique task name
        # This Bash command changes the directory to the dbt project location inside Airflow,
        # then runs dbt to transform data, specifically targeting the "refined_ranking" model only.
        bash_command='cd /opt/airflow/my_dbt_project && dbt run --select refined_ranking'
    )

    # Define task dependencies: task_ingest must finish before task_transform runs
    task_ingest >> task_transform