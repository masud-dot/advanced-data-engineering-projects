-- Target warehouse upsert.
-- Run after staging the incremental dataset.

INSERT INTO warehouse_transactions (
    transaction_id,
    customer_id,
    amount,
    created_at,
    updated_at
)
SELECT
    transaction_id,
    customer_id,
    amount,
    created_at,
    updated_at
FROM staging_transactions
ON CONFLICT (transaction_id)
DO UPDATE SET
    customer_id = EXCLUDED.customer_id,
    amount = EXCLUDED.amount,
    created_at = EXCLUDED.created_at,
    updated_at = EXCLUDED.updated_at;
