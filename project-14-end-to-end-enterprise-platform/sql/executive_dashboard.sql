COPY fact_sales FROM 's3://enterprise-platform/gold/' IAM_ROLE 'arn:aws:iam::123456789012:role/redshift-role' FORMAT AS PARQUET;
SELECT sale_date,region,SUM(total_revenue) AS revenue,SUM(order_count) AS orders,AVG(total_revenue) AS avg_order_value FROM fact_sales WHERE sale_date>=DATEADD(day,-30,GETDATE()) GROUP BY sale_date,region ORDER BY sale_date DESC,revenue DESC;
