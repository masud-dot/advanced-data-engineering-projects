-- Project 10: CI/CD Data Validation
--
-- Example validation checks that can be executed
-- against a production warehouse after deployment.

-- 1. Row count
SELECT COUNT(*) AS row_count
FROM processed_sales;

-- 2. Null transaction IDs
SELECT COUNT(*) AS null_transaction_ids
FROM processed_sales
WHERE transaction_id IS NULL;

-- 3. Negative amounts
SELECT COUNT(*) AS invalid_amounts
FROM processed_sales
WHERE amount < 0;

-- 4. Duplicate transaction IDs
SELECT
    transaction_id,
    COUNT(*) AS duplicate_count
FROM processed_sales
GROUP BY transaction_id
HAVING COUNT(*) > 1;

-- 5. Calculation validation
SELECT COUNT(*) AS calculation_errors
FROM processed_sales
WHERE ROUND(total_amount, 2)
      <> ROUND(amount + tax_amount, 2);
