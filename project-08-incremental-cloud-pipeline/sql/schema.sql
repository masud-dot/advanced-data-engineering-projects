CREATE TABLE customer_transactions (transaction_id BIGINT PRIMARY KEY, customer_id INT, amount NUMERIC(12,2), created_at TIMESTAMP, updated_at TIMESTAMP);
CREATE TABLE pipeline_metadata (pipeline_name VARCHAR(100) PRIMARY KEY, last_watermark TIMESTAMP);
INSERT INTO pipeline_metadata VALUES ('incremental_cloud_pipeline','2026-01-01 00:00:00');
