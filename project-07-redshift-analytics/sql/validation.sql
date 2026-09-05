-- Project 07: Data-quality and warehouse validation queries.

-- Row count.
SELECT COUNT(*) AS total_rows
FROM fact_sales;


-- Check for null business keys.
SELECT COUNT(*) AS invalid_rows
FROM fact_sales
WHERE sale_id IS NULL
   OR customer_id IS NULL
   OR product_id IS NULL
   OR amount IS NULL
   OR region IS NULL
   OR sale_date IS NULL;


-- Check for invalid sales amounts.
SELECT COUNT(*) AS invalid_amount_rows
FROM fact_sales
WHERE amount < 0;


-- Check for duplicate sale IDs.
SELECT
    sale_id,
    COUNT(*) AS duplicate_count
FROM fact_sales
GROUP BY sale_id
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;


-- Check date coverage.
SELECT
    MIN(sale_date) AS earliest_sale,
    MAX(sale_date) AS latest_sale
FROM fact_sales;


-- Basic warehouse summary.
SELECT
    COUNT(*) AS total_transactions,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(DISTINCT product_id) AS unique_products,
    SUM(amount) AS total_sales
FROM fact_sales;
