-- Project 09: Bronze layer
-- Bronze preserves raw source records with minimal transformation.

CREATE EXTERNAL TABLE IF NOT EXISTS bronze_sales (
    transaction_id BIGINT,
    customer_id INT,
    product_id STRING,
    amount DECIMAL(12,2),
    event_time TIMESTAMP,
    region STRING,
    year INT,
    month INT,
    day INT
)
STORED AS PARQUET
LOCATION 's3://enterprise-lakehouse/bronze/';
