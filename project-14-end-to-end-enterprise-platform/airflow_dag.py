from airflow import DAG
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from datetime import datetime,timedelta
default_args={'retries':3,'retry_delay':timedelta(minutes=10)}
with DAG('enterprise_platform',schedule_interval='@daily',start_date=datetime(2026,1,1),default_args=default_args) as dag:
    silver_etl=GlueJobOperator(task_id='silver_etl',job_name='silver_transformation')
    gold_agg=GlueJobOperator(task_id='gold_aggregation',job_name='gold_business_metrics')
    load_redshift=S3ToRedshiftOperator(task_id='load_to_redshift',s3_bucket='enterprise-platform',s3_key='gold/',schema='public',table='fact_sales',copy_options=['FORMAT AS PARQUET'])
    silver_etl >> gold_agg >> load_redshift
