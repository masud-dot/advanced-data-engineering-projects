-- Enterprise Data Platform Analytics
-- These queries target the Gold/warehouse layer.

-- 1. Daily revenue and order performance
SELECT
    order_date,
    region,
    SUM(revenue) AS total_revenue,
    COUNT(DISTINCT order_id) AS order_count,
    ROUND(
        SUM(revenue) / NULLIF(COUNT(DISTINCT order_id), 0),
        2
    ) AS average_order_value
FROM fact_orders
GROUP BY order_date, region
ORDER BY order_date DESC, total_revenue DESC;


-- 2. Top products by revenue
SELECT
    product_id,
    SUM(revenue) AS total_revenue,
    SUM(quantity) AS units_sold,
    COUNT(DISTINCT order_id) AS order_count
FROM fact_orders
GROUP BY product_id
ORDER BY total_revenue DESC
LIMIT 10;


-- 3. Customer revenue ranking
SELECT
    customer_id,
    COUNT(DISTINCT order_id) AS order_count,
    SUM(revenue) AS total_revenue,
    ROUND(
        SUM(revenue) / NULLIF(COUNT(DISTINCT order_id), 0),
        2
    ) AS average_order_value
FROM fact_orders
GROUP BY customer_id
ORDER BY total_revenue DESC;


-- 4. Regional performance
SELECT
    region,
    SUM(revenue) AS total_revenue,
    COUNT(DISTINCT order_id) AS order_count,
    SUM(quantity) AS units_sold
FROM fact_orders
GROUP BY region
ORDER BY total_revenue DESC;


-- 5. Category performance
SELECT
    category,
    SUM(revenue) AS total_revenue,
    SUM(quantity) AS units_sold,
    COUNT(DISTINCT order_id) AS order_count
FROM fact_orders
GROUP BY category
ORDER BY total_revenue DESC;


-- 6. Executive KPI summary
SELECT
    SUM(revenue) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS active_customers,
    SUM(quantity) AS total_units_sold,
    ROUND(
        SUM(revenue) / NULLIF(COUNT(DISTINCT order_id), 0),
        2
    ) AS average_order_value
FROM fact_orders;
