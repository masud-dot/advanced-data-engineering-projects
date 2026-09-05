-- Project 08: Incremental Cloud Pipeline
-- Source and pipeline-control tables.

DROP TABLE IF EXISTS customer_transactions;
DROP TABLE IF EXISTS pipeline_metadata;

CREATE TABLE customer_transactions (
    transaction_id BIGINT PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE pipeline_metadata (
    pipeline_name VARCHAR(100) PRIMARY KEY,
    last_watermark TIMESTAMP NOT NULL
);

INSERT INTO pipeline_metadata (
    pipeline_name,
    last_watermark
)
VALUES (
    'incremental_cloud_pipeline',
    '2026-01-01 00:00:00'
);
