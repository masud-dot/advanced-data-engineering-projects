-- Project 07: Redshift Analytics Warehouse
-- Warehouse schema for sales analytics.

DROP TABLE IF EXISTS fact_sales;

CREATE TABLE fact_sales (
    sale_id      BIGINT          NOT NULL,
    customer_id  INTEGER         NOT NULL,
    product_id   INTEGER         NOT NULL,
    amount       NUMERIC(12,2)   NOT NULL,
    region       VARCHAR(50)     NOT NULL,
    sale_date    DATE            NOT NULL
)
DISTSTYLE KEY
DISTKEY (customer_id)
SORTKEY (sale_date);
