import os
import boto3
import pandas as pd
from datetime import date

BUCKET = os.getenv('S3_BUCKET','enterprise-data-lake')
s3 = boto3.client('s3')
today = date.today()

s3_key = f'bronze/sales/year={today.year}/month={today.month:02d}/day={today.day:02d}/sales_data.csv'
s3.upload_file('datasets/sales_data.csv', BUCKET, s3_key)
print(f'Uploaded: s3://{BUCKET}/{s3_key}')

df = pd.read_csv('datasets/sales_data.csv').drop_duplicates().dropna()
df['total_amount'] = df['quantity'] * df['price']
df.to_parquet('processed_sales.parquet', index=False)
s3.upload_file('processed_sales.parquet', BUCKET, 'silver/cleaned_sales/processed_sales.parquet')

summary = df.groupby('region')['total_amount'].sum().reset_index()
summary.columns = ['region','total_sales']
summary.to_parquet('regional_summary.parquet', index=False)
s3.upload_file('regional_summary.parquet', BUCKET, 'gold/analytics/regional_sales_summary.parquet')
