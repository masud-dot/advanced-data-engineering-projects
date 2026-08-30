SELECT product_id, SUM(total_sales) AS revenue, SUM(order_count) AS orders, AVG(avg_order_value) AS avg_value FROM gold_sales GROUP BY product_id ORDER BY revenue DESC LIMIT 20;
