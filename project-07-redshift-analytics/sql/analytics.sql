-- Project 07: Analytical SQL examples.

-- 1. Regional sales performance.
SELECT
    region,
    SUM(amount) AS total_sales,
    COUNT(*) AS transaction_count,
    ROUND(
        SUM(amount) / NULLIF(COUNT(*), 0),
        2
    ) AS average_transaction_value
FROM fact_sales
WHERE sale_date >= DATE '2026-01-01'
GROUP BY region
ORDER BY total_sales DESC;


-- 2. Daily sales trend.
SELECT
    sale_date,
    SUM(amount) AS daily_sales,
    COUNT(*) AS transaction_count
FROM fact_sales
GROUP BY sale_date
ORDER BY sale_date;


-- 3. Top 10 customers by lifetime sales.
SELECT
    customer_id,
    SUM(amount) AS total_spent,
    COUNT(*) AS purchase_count
FROM fact_sales
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10;


-- 4. Monthly sales performance.
SELECT
    DATE_TRUNC('month', sale_date)::DATE AS sales_month,
    SUM(amount) AS monthly_sales
FROM fact_sales
GROUP BY 1
ORDER BY 1;


-- 5. Regional monthly performance.
SELECT
    DATE_TRUNC('month', sale_date)::DATE AS sales_month,
    region,
    SUM(amount) AS regional_sales
FROM fact_sales
GROUP BY 1, 2
ORDER BY 1, regional_sales DESC;


-- 6. Product performance.
SELECT
    product_id,
    SUM(amount) AS product_sales,
    COUNT(*) AS transaction_count
FROM fact_sales
GROUP BY product_id
ORDER BY product_sales DESC;


-- 7. Running sales total.
SELECT
    sale_date,
    daily_sales,
    SUM(daily_sales) OVER (
        ORDER BY sale_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_sales
FROM (
    SELECT
        sale_date,
        SUM(amount) AS daily_sales
    FROM fact_sales
    GROUP BY sale_date
) daily
ORDER BY sale_date;
