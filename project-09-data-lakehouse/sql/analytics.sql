-- Project 09: Lakehouse analytics queries.

-- 1. Top products by revenue.
SELECT
    product_id,
    total_sales,
    order_count,
    avg_order_value
FROM gold_sales
ORDER BY total_sales DESC
LIMIT 20;

-- 2. Products with more than five orders.
SELECT
    product_id,
    total_sales,
    order_count
FROM gold_sales
WHERE order_count > 5
ORDER BY total_sales DESC;

-- 3. Average order value by product.
SELECT
    product_id,
    ROUND(avg_order_value, 2) AS avg_order_value
FROM gold_sales
ORDER BY avg_order_value DESC;

-- 4. Revenue contribution by product.
SELECT
    product_id,
    total_sales,
    ROUND(
        100.0 * total_sales
        / SUM(total_sales) OVER (),
        2
    ) AS revenue_percentage
FROM gold_sales
ORDER BY total_sales DESC;
