import os
import subprocess
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def run_fetch_stock_data():
    # Path inside Airflow container
    subprocess.run(["python", "/opt/airflow/dags/fetch_stock_data.py"], check=True)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='stock_pipeline',
    default_args=default_args,
    description='Fetch stock data hourly and store in Postgres',
    schedule_interval='@hourly',
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['stocks'],
) as dag:

    fetch_task = PythonOperator(
        task_id='fetch_stock_data',
        python_callable=run_fetch_stock_data
    )
