SELECT region, SUM(amount) AS total_sales FROM fact_sales WHERE sale_date >= '2026-01-01' GROUP BY region ORDER BY total_sales DESC;

SELECT sale_date, SUM(amount) AS daily_sales FROM fact_sales GROUP BY sale_date ORDER BY sale_date;

SELECT customer_id, SUM(amount) AS total_spent FROM fact_sales GROUP BY customer_id ORDER BY total_spent DESC LIMIT 10;
