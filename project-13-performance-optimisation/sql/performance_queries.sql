-- Project 13: Pipeline Performance Optimisation
-- Example SQL patterns for identifying performance bottlenecks,
-- reducing scanned data, and validating query efficiency.

-- 1. Aggregate transactions by date.
SELECT
    transaction_date,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount,
    AVG(amount) AS average_amount
FROM sales_data
GROUP BY transaction_date
ORDER BY transaction_date;


-- 2. Filter early to reduce the amount of data processed.
SELECT
    transaction_id,
    customer_id,
    product_id,
    transaction_date,
    amount
FROM sales_data
WHERE status = 'COMPLETED'
  AND transaction_date >= '2026-09-01';


-- 3. Aggregate by customer.
SELECT
    customer_id,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount
FROM sales_data
WHERE status = 'COMPLETED'
GROUP BY customer_id
ORDER BY total_amount DESC;


-- 4. Partition-aware filtering.
-- In partitioned data systems, filtering on the partition column
-- can significantly reduce the amount of data scanned.
SELECT
    transaction_id,
    customer_id,
    amount
FROM sales_data
WHERE transaction_date = '2026-09-03';


-- 5. Identify high-value transactions.
SELECT
    transaction_id,
    customer_id,
    amount,
    transaction_date
FROM sales_data
WHERE amount >= 4000
ORDER BY amount DESC;


-- 6. Performance validation query.
SELECT
    status,
    COUNT(*) AS row_count,
    SUM(amount) AS total_amount
FROM sales_data
GROUP BY status
ORDER BY row_count DESC;
