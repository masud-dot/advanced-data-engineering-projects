import os
import pandas as pd
from sqlalchemy import create_engine, text

engine=create_engine(os.getenv('DATABASE_URL','postgresql://postgres:admin@localhost:5432/data_engineering'))
watermark=pd.read_sql("SELECT last_watermark FROM pipeline_metadata WHERE pipeline_name='incremental_cloud_pipeline'",engine).iloc[0,0]
incremental_df=pd.read_sql(f"SELECT * FROM customer_transactions WHERE updated_at > '{watermark}'",engine)
incremental_df=incremental_df.drop_duplicates(subset=['transaction_id'],keep='last')
for part in ['year','month','day']:
    incremental_df[part]=pd.to_datetime(incremental_df['updated_at']).dt.__getattribute__(part)

# Write with pyarrow/s3fs in a real AWS environment.
incremental_df.to_parquet('incremental_output.parquet',index=False)

# Update watermark only after the downstream load/upsert succeeds.
with engine.connect() as conn:
    conn.execute(text("UPDATE pipeline_metadata SET last_watermark=NOW() WHERE pipeline_name='incremental_cloud_pipeline'"))
    conn.commit()
