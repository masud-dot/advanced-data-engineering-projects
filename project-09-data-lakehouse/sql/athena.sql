-- Project 09: Amazon Athena examples.

-- Top products.
SELECT
    product_id,
    total_sales AS revenue,
    order_count AS orders,
    avg_order_value AS avg_value
FROM gold_sales
ORDER BY revenue DESC
LIMIT 20;

-- Revenue by region from Silver.
SELECT
    region,
    SUM(amount) AS revenue,
    COUNT(*) AS orders,
    AVG(amount) AS avg_order_value
FROM silver_sales
GROUP BY region
ORDER BY revenue DESC;

-- Monthly revenue.
SELECT
    year,
    month,
    SUM(amount) AS revenue,
    COUNT(*) AS orders
FROM silver_sales
GROUP BY year, month
ORDER BY year, month;
