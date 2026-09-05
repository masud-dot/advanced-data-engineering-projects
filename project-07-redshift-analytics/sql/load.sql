-- Project 07: Bulk load sales data from Amazon S3.
--
-- Replace YOUR_IAM_ROLE_ARN with the IAM role attached to
-- the Redshift cluster/workgroup.
--
-- The S3 location should contain the synthetic sales CSV
-- used by this project.

COPY fact_sales
FROM 's3://enterprise-redshift-warehouse/raw/sales_data.csv'
IAM_ROLE 'YOUR_IAM_ROLE_ARN'
FORMAT AS CSV
IGNOREHEADER 1
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
COMPUPDATE ON
STATUPDATE ON;
