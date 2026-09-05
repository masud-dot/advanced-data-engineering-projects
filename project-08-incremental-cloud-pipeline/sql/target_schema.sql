-- Target warehouse table for incremental upsert processing.

CREATE TABLE warehouse_transactions (
    transaction_id BIGINT PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
