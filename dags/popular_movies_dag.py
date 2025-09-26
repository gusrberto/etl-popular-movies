from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from etl.transform import transform
from etl.load import load

def run_transform(**kwargs):
    import os
    df = transform()
    path = "/opt/airflow/movies.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_json(path, orient="records")
    return path

def run_load(ti=None, **kwargs):
    import pandas as pd
    path = ti.xcom_pull(task_ids="transform_task")
    df = pd.read_json(path)
    load(df, airflow=True)

with DAG(
    dag_id="etl_movies_dag",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",  # roda todo dia
    catchup=False,
) as dag:

    transform_task = PythonOperator(
        task_id="transform_task",
        python_callable=run_transform,
    )

    load_task = PythonOperator(
        task_id="load_task",
        python_callable=run_load,
    )

    transform_task >> load_task
