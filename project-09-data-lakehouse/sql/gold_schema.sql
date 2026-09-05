-- Project 09: Gold layer
-- Gold contains business-ready product sales metrics.

CREATE EXTERNAL TABLE IF NOT EXISTS gold_sales (
    product_id STRING,
    total_sales DECIMAL(18,2),
    order_count BIGINT,
    avg_order_value DECIMAL(18,2)
)
STORED AS PARQUET
LOCATION 's3://enterprise-lakehouse/gold/';
