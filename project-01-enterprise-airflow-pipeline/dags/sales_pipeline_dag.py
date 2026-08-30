from datetime import datetime, timedelta

import pandas as pd
from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator

from pipelines.extract import extract_data
from pipelines.transform import transform_data
from pipelines.load import load_data


def run_extract(**kwargs):
    df = extract_data("/opt/airflow/datasets/sales_data.csv")
    kwargs["ti"].xcom_push(key="raw_data", value=df.to_json())


def run_transform(**kwargs):
    raw_json = kwargs["ti"].xcom_pull(
        task_ids="extract_data",
        key="raw_data",
    )
    df = pd.read_json(raw_json)
    transformed_df = transform_data(df)

    kwargs["ti"].xcom_push(
        key="transformed_data",
        value=transformed_df.to_json(date_format="iso"),
    )


def run_load(**kwargs):
    transformed_json = kwargs["ti"].xcom_pull(
        task_ids="transform_data",
        key="transformed_data",
    )

    from io import StringIO

    transformed_df = pd.read_json(StringIO(transformed_json))

    if "order_date" in transformed_df.columns:
        transformed_df["order_date"] = (
            pd.to_datetime(transformed_df["order_date"], errors="raise")
            .dt.date
        )

    load_data(transformed_df)


with DAG(
    dag_id="enterprise_sales_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={
        "owner": "data_engineer",
        "retries": 3,
        "retry_delay": timedelta(minutes=5),
    },
) as dag:

    extract_task = PythonOperator(
        task_id="extract_data",
        python_callable=run_extract,
    )

    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=run_transform,
    )

    load_task = PythonOperator(
        task_id="load_data",
        python_callable=run_load,
    )

    extract_task >> transform_task >> load_task
