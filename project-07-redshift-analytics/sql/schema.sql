CREATE TABLE fact_sales (
    sale_id BIGINT, customer_id INT, product_id INT, amount NUMERIC(12,2), region VARCHAR(50), sale_date DATE
) DISTKEY(customer_id) SORTKEY(sale_date);
