COPY fact_sales
FROM 's3://enterprise-redshift-warehouse/raw/sales_data.csv'
IAM_ROLE 'arn:aws:iam::123456789012:role/redshift-s3-role'
CSV IGNOREHEADER 1;
