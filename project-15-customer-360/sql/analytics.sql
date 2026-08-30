CREATE TABLE fact_orders AS SELECT o.order_id,o.customer_id,o.amount,o.order_date,c.country,c.segment FROM orders o JOIN customers c ON o.customer_id=c.customer_id;
SELECT country,SUM(amount) AS revenue,COUNT(*) AS orders FROM fact_orders GROUP BY country ORDER BY revenue DESC;
