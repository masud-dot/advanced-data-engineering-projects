CREATE TABLE IF NOT EXISTS sales_data (
    order_id VARCHAR(20),
    customer_name VARCHAR(100),
    product_name VARCHAR(100),
    quantity INT,
    price NUMERIC,
    order_date DATE,
    region VARCHAR(50),
    total_amount NUMERIC
);
