# Project 07 — Redshift Analytics Warehouse

A production-oriented Amazon Redshift analytics warehouse project demonstrating fact-table design, Amazon S3 bulk loading, analytical SQL, data validation, distribution and sort strategies, and practical query optimization patterns.

The repository uses synthetic sales data and parameterized AWS configuration so the implementation can be safely used as a learning and portfolio project.

## Architecture

Amazon S3
    |
    | CSV sales data
    v
Redshift COPY
    |
    v
fact_sales
    |
    +--> Regional Sales Analytics
    +--> Daily Sales Trends
    +--> Customer Analytics
    +--> Product Analytics
    +--> Monthly Analytics
    +--> Data Quality Validation

## Technology

- Amazon Redshift
- Amazon S3
- SQL
- Redshift COPY
- Distribution Keys
- Sort Keys
- Window Functions
- Aggregations
- Git and GitHub

## Project Structure

```text
project-07-redshift-analytics/
|
+-- README.md
+-- .gitignore
+-- sample_data/
|   +-- sales_data.csv
|
+-- sql/
    +-- schema.sql
    +-- load.sql
    +-- analytics.sql
    +-- validation.sql
```

## Business Scenario

Assume an enterprise organization receives sales transactions as CSV files in Amazon S3.

The data engineering team needs to:

1. Load the data into Amazon Redshift.
2. Store it in an analytics-friendly fact table.
3. Optimize the table for common query patterns.
4. Produce regional, customer, product, daily, and monthly analytics.
5. Validate data quality.
6. Provide a repeatable SQL-based warehouse workflow.

## Source Data

The sample dataset is available at:

`sample_data/sales_data.csv`

Example production S3 location:

`s3://enterprise-redshift-warehouse/raw/sales_data.csv`

The dataset is synthetic and contains no production or personal data.

## Source Schema

| Column | Type | Description |
|---|---|---|
| `sale_id` | BIGINT | Unique sale identifier |
| `customer_id` | INTEGER | Customer identifier |
| `product_id` | INTEGER | Product identifier |
| `amount` | NUMERIC(12,2) | Transaction amount |
| `region` | VARCHAR(50) | Sales region |
| `sale_date` | DATE | Date of transaction |

## Warehouse Schema

The main warehouse table is `fact_sales`.

It uses:

- `DISTKEY(customer_id)`
- `SORTKEY(sale_date)`

### Distribution Key

`customer_id` is used as the distribution key to demonstrate customer-oriented warehouse workloads.

In production, the distribution strategy should be selected using actual table sizes, join patterns, query workloads, and Redshift recommendations.

### Sort Key

`sale_date` is used as the sort key because time-based filtering is common in analytical workloads.

Queries filtering by date can benefit from a table organized around the date column.

## SQL Workflow

1. Run `sql/schema.sql`.
2. Upload `sample_data/sales_data.csv` to Amazon S3.
3. Configure the IAM role used by Redshift.
4. Run `sql/load.sql`.
5. Run `sql/validation.sql`.
6. Run analytical queries from `sql/analytics.sql`.

## Step 1 — Create the Warehouse Table

Execute:

`sql/schema.sql`

This creates the `fact_sales` table with numeric transaction amounts and date-based sorting.

## Step 2 — Upload Data to Amazon S3

Upload:

`sample_data/sales_data.csv`

to your configured S3 location.

Example:

`s3://enterprise-redshift-warehouse/raw/sales_data.csv`

## Step 3 — Configure IAM Access

Redshift requires permission to read the S3 source data.

The IAM role attached to the Redshift cluster or Serverless workgroup should have the minimum required permissions for the source S3 location.

Do not place AWS access keys or secret keys inside SQL files.

The repository uses this placeholder in `sql/load.sql`:

`YOUR_IAM_ROLE_ARN`

Replace it only in your local or deployment copy with the appropriate IAM role ARN.

## Step 4 — Bulk Load with COPY

The `sql/load.sql` script uses the Redshift `COPY` command to load CSV data from Amazon S3.

The load configuration includes:

- CSV format
- Header-row handling
- Automatic date parsing
- Compression analysis
- Statistics update

Example:

```text
COPY fact_sales
FROM 's3://enterprise-redshift-warehouse/raw/sales_data.csv'
IAM_ROLE 'YOUR_IAM_ROLE_ARN'
FORMAT AS CSV
IGNOREHEADER 1
DATEFORMAT 'auto'
TIMEFORMAT 'auto'
COMPUPDATE ON
STATUPDATE ON;
```

Change the S3 location and IAM role for an actual deployment.

## Step 5 — Validate the Warehouse

Execute:

`sql/validation.sql`

The validation queries check:

- Total row count
- Null business fields
- Invalid amounts
- Duplicate sale IDs
- Date coverage
- Overall warehouse statistics

## Analytical Queries

`sql/analytics.sql` contains practical analytics patterns.

### Regional Sales

Calculates total sales, transaction count, and average transaction value by region.

### Daily Sales Trend

Shows daily sales and transaction volume.

### Top Customers

Ranks customers by total spending.

### Monthly Sales

Aggregates sales by calendar month.

### Regional Monthly Performance

Combines month and region for time-based regional analysis.

### Product Performance

Ranks products by sales amount and transaction count.

### Running Sales Total

Uses a window function to calculate cumulative sales over time.

## Query Optimization Concepts

### Distribution Strategy

The fact table uses `DISTKEY(customer_id)` to demonstrate distribution-key selection for customer-oriented workloads.

The best production distribution strategy depends on the actual workload.

### Sort Strategy

The fact table uses `SORTKEY(sale_date)` to support common date-range filtering patterns.

### Predicate Filtering

Date predicates are applied where appropriate to reduce the data participating in analytical queries.

### Column Selection

Queries select only the columns required for each analytical calculation.

### Aggregation

Aggregations are performed in Redshift rather than moving large datasets outside the warehouse.

### Window Functions

The cumulative-sales query demonstrates analytical processing using SQL window functions.

## Production Considerations

### Redshift Provisioning

The project can be adapted for:

- Amazon Redshift provisioned clusters
- Amazon Redshift Serverless

Connection and IAM configuration depends on the deployment model.

### IAM

Use IAM roles rather than embedding AWS credentials.

Follow least-privilege access for Amazon S3, Redshift, and other services used by the platform.

### S3 Organization

A recommended structure is:

```text
s3://enterprise-redshift-warehouse/
|
+-- raw/
|   +-- sales_data.csv
|
+-- archive/
|
+-- rejected/
```

### Data Quality

Production pipelines should add:

- Schema validation
- Duplicate detection
- Referential integrity
- Accepted-value validation
- Amount-range validation
- Freshness checks
- Row-count reconciliation

### Workload Monitoring

Monitor:

- Query duration
- Queue time
- Scan volume
- Table statistics
- Sort quality
- Distribution skew
- Concurrency
- Storage utilization

Optimization decisions should be based on actual workload measurements.

## Local Testing

Amazon Redshift itself is not executed by the local sample-data workflow.

The included CSV is provided for reviewing the source structure, understanding the warehouse model, preparing an S3 load, and reproducing the example queries in Redshift.

The Redshift-specific SQL should be executed against Amazon Redshift rather than SQLite because features such as `DISTKEY`, `SORTKEY`, and `COPY` are Redshift-specific.

## Sample Dataset

The sample dataset contains 15 synthetic sales transactions across multiple regions and dates.

It exercises:

- Regional aggregation
- Customer aggregation
- Product aggregation
- Daily trends
- Monthly trends
- Window-function analysis

## Security

Never commit:

- AWS access keys
- AWS secret keys
- IAM credentials
- Database passwords
- Production connection strings
- Cloud account secrets
- Production datasets

The IAM role in `sql/load.sql` is intentionally represented by:

`YOUR_IAM_ROLE_ARN`

Use your organization's approved IAM and secret-management process for actual deployments.

## Troubleshooting

### COPY Permission Error

If `COPY` cannot read the S3 object:

1. Verify the S3 path.
2. Verify the Redshift IAM role.
3. Confirm the role can read the required S3 object.
4. Confirm the role is associated with the Redshift environment.

### Invalid Data Type

If loading fails because of a data-type mismatch:

1. Inspect the source CSV.
2. Confirm column order.
3. Check numeric fields.
4. Check date values.
5. Verify `sql/schema.sql`.

### Duplicate Records

Run the duplicate validation query in `sql/validation.sql`.

### Poor Query Performance

Check:

- Distribution strategy
- Sort-key strategy
- Table statistics
- Query predicates
- Data distribution/skew
- Query execution plans

Avoid changing distribution or sort keys without understanding the workload.

## Files

### `sql/schema.sql`

Creates the Redshift `fact_sales` warehouse table.

### `sql/load.sql`

Loads sales data from Amazon S3 using Redshift `COPY`.

### `sql/analytics.sql`

Contains practical analytical SQL examples.

### `sql/validation.sql`

Contains warehouse and data-quality validation queries.

### `sample_data/sales_data.csv`

Synthetic sales data for the project.

## Book Reference

This repository is the companion implementation for:

**Advanced Data Engineering Projects with Python, SQL & Cloud**

The project demonstrates:

- Amazon Redshift
- Amazon S3
- Fact-table design
- Distribution keys
- Sort keys
- Bulk loading
- Analytical SQL
- Aggregations
- Window functions
- Data-quality validation
- Query optimization
- Production-oriented cloud data engineering

## License

This project is provided for educational and demonstration purposes.
