-- Source system schema used by the incremental extraction process.

CREATE TABLE customer_transactions (
    transaction_id BIGINT PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
