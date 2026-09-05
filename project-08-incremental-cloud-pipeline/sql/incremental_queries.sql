-- Incremental extraction and monitoring queries.

-- 1. Extract records newer than the stored watermark.
SELECT
    transaction_id,
    customer_id,
    amount,
    created_at,
    updated_at
FROM customer_transactions
WHERE updated_at > :last_watermark
ORDER BY updated_at, transaction_id;

-- 2. Identify the next watermark.
SELECT MAX(updated_at) AS next_watermark
FROM customer_transactions
WHERE updated_at > :last_watermark;

-- 3. Check the current pipeline watermark.
SELECT
    pipeline_name,
    last_watermark
FROM pipeline_metadata
WHERE pipeline_name = 'incremental_cloud_pipeline';

-- 4. Detect duplicate transaction IDs.
SELECT
    transaction_id,
    COUNT(*) AS duplicate_count
FROM customer_transactions
GROUP BY transaction_id
HAVING COUNT(*) > 1;

-- 5. Check records updated after the current watermark.
SELECT COUNT(*) AS pending_incremental_rows
FROM customer_transactions c
JOIN pipeline_metadata p
  ON p.pipeline_name = 'incremental_cloud_pipeline'
WHERE c.updated_at > p.last_watermark;
