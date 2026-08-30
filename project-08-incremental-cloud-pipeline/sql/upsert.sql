INSERT INTO warehouse_transactions SELECT * FROM staging_transactions
ON CONFLICT (transaction_id) DO UPDATE SET amount=EXCLUDED.amount, updated_at=EXCLUDED.updated_at;
