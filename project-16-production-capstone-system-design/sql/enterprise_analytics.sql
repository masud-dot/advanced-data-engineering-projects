-- Production warehouse query examples.
-- These queries are written for the Redshift-equivalent analytics layer.

-- Total transaction value by customer
SELECT
    customer_id,
    customer_name,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_value,
    AVG(amount) AS average_transaction_value
FROM fact_transactions
GROUP BY customer_id, customer_name
ORDER BY total_value DESC;

-- Fraud summary
SELECT
    fraud_flag,
    COUNT(*) AS transaction_count,
    SUM(amount) AS transaction_value
FROM fact_transactions
GROUP BY fraud_flag
ORDER BY fraud_flag DESC;

-- Merchant category performance
SELECT
    merchant_category,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_value
FROM fact_transactions
GROUP BY merchant_category
ORDER BY total_value DESC;
