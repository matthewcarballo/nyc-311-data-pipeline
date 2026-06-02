from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, '/Users/matthewcarballo/Desktop/nyc-311-data-pipeline')

from ingestion.fetch_311_data import fetch_311_data, save_to_csv, load_to_postgres

default_args = {
    'owner': 'matthew',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def run_fetch_and_save():
    data = fetch_311_data(limit=1000)
    filename = save_to_csv(data)
    return filename

def run_load_to_postgres():
    import glob
    files = glob.glob('data/raw_311_*.csv')
    latest_file = max(files)
    load_to_postgres(latest_file)

with DAG(
    dag_id='nyc_311_pipeline',
    default_args=default_args,
    description='Daily pipeline to fetch and load NYC 311 data',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:

    fetch_task = PythonOperator(
        task_id='fetch_and_save',
        python_callable=run_fetch_and_save
    )

    load_task = PythonOperator(
        task_id='load_to_postgres',
        python_callable=run_load_to_postgres
    )

    fetch_task >> load_task