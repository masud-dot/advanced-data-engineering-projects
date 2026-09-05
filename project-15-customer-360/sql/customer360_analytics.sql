-- Customer 360 Unified Analytics Platform
-- Business-ready SQL analytics examples

-- 1. Customer lifetime value
SELECT
    customer_id,
    customer_name,
    customer_segment,
    lifetime_value,
    order_count,
    average_order_value
FROM customer_360_profile
ORDER BY lifetime_value DESC;


-- 2. Revenue by region
SELECT
    region,
    COUNT(DISTINCT customer_id) AS customer_count,
    SUM(lifetime_value) AS total_revenue,
    AVG(lifetime_value) AS average_customer_value
FROM customer_360_profile
GROUP BY region
ORDER BY total_revenue DESC;


-- 3. Customer segment performance
SELECT
    customer_segment,
    COUNT(DISTINCT customer_id) AS customer_count,
    SUM(lifetime_value) AS total_revenue,
    AVG(lifetime_value) AS average_revenue,
    AVG(order_count) AS average_orders,
    AVG(engagement_score) AS average_engagement
FROM customer_360_profile
GROUP BY customer_segment
ORDER BY total_revenue DESC;


-- 4. Product category performance
SELECT
    category,
    COUNT(DISTINCT order_id) AS order_count,
    SUM(quantity) AS total_units,
    SUM(revenue) AS total_revenue
FROM fact_customer_transactions
GROUP BY category
ORDER BY total_revenue DESC;


-- 5. Top customers
SELECT
    customer_id,
    customer_name,
    region,
    customer_segment,
    lifetime_value,
    order_count,
    engagement_score
FROM customer_360_profile
ORDER BY lifetime_value DESC
LIMIT 10;


-- 6. At-risk customers
SELECT
    customer_id,
    customer_name,
    email,
    region,
    lifetime_value,
    order_count,
    recency_days,
    engagement_score
FROM customer_360_profile
WHERE customer_segment = 'AT_RISK'
ORDER BY lifetime_value DESC;


-- 7. Highly engaged customers
SELECT
    customer_id,
    customer_name,
    customer_segment,
    engagement_score,
    lifetime_value,
    order_count
FROM customer_360_profile
WHERE engagement_score >= 8
ORDER BY engagement_score DESC, lifetime_value DESC;


-- 8. Recent transactions
SELECT
    order_id,
    customer_id,
    product_name,
    category,
    quantity,
    revenue,
    order_date
FROM fact_customer_transactions
WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY order_date DESC;
