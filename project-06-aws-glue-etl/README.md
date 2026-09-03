# Project 06 — AWS Glue ETL Pipeline

A production-style AWS Glue ETL pipeline that reads sales data from the AWS Glue Data Catalog, cleans and transforms the data with PySpark, calculates transaction totals, creates regional sales aggregations, and writes partitioned Parquet datasets to Amazon S3.

This project also includes a local PySpark test implementation so the transformation logic can be validated without an AWS account.

## Architecture

S3 Raw Data
    |
    v
AWS Glue Crawler
    |
    v
AWS Glue Data Catalog
    |
    v
AWS Glue ETL Job
    |
    +--> Data Cleaning
    |
    +--> Duplicate Removal
    |
    +--> Data Validation
    |
    +--> Total Amount Calculation
    |
    +--> Regional Aggregation
    |
    v
Amazon S3
    |
    +--> Processed Sales - Partitioned by Region
    |
    +--> Regional Sales Summary

## Technology

- AWS Glue
- AWS Glue Data Catalog
- AWS Glue Crawlers
- PySpark
- Amazon S3
- Apache Parquet
- Python
- Git and GitHub

## Project Structure

```text
project-06-aws-glue-etl/
|
+-- README.md
+-- crawler_config.md
+-- glue_job.py
+-- transformations.py
+-- local_test.py
+-- sample_data/
|   +-- sales_data.csv
|
+-- .gitignore
```

## Source Data

The production Glue job expects sales data to be registered in the AWS Glue Data Catalog.

Default catalog configuration:

- Database: `enterprise_db`
- Table: `sales_data`

The corresponding S3 source location is:

`s3://enterprise-etl-bucket/raw/sales_data/`

## Expected Source Schema

| Column | Type | Description |
|---|---|---|
| `order_id` | Integer | Unique order identifier |
| `customer_id` | Integer | Customer identifier |
| `region` | String | Sales region |
| `product` | String | Product name |
| `quantity` | Integer | Quantity purchased |
| `price` | Double | Unit price |
| `order_date` | String/Date | Order date |

## ETL Processing

The Glue job performs the following operations:

1. Reads data from the AWS Glue Data Catalog.
2. Validates the required columns.
3. Removes duplicate records.
4. Removes records containing required null values.
5. Removes records with invalid quantities.
6. Removes records with negative prices.
7. Calculates `total_amount`.
8. Adds a UTC processing timestamp.
9. Aggregates sales by region.
10. Writes detailed data as partitioned Parquet.
11. Writes the regional summary as Parquet.
12. Commits the AWS Glue job.

## Transformation Logic

The transaction amount is calculated as:

`total_amount = quantity * price`

Regional sales are calculated using:

`SUM(total_amount) GROUP BY region`

The detailed output is partitioned by:

`region`

This partitioning strategy allows downstream analytics workloads to scan only the required regional data.

## AWS Glue Job Configuration

The production job uses these configurable values:

| Parameter | Default |
|---|---|
| `JOB_NAME` | Required |
| `SOURCE_PATH` | `s3://enterprise-etl-bucket/raw/sales_data/` |
| `OUTPUT_PATH` | `s3://enterprise-etl-bucket/processed/sales/` |
| `SUMMARY_PATH` | `s3://enterprise-etl-bucket/processed/regional_summary/` |
| `GLUE_DATABASE` | `enterprise_db` |
| `GLUE_TABLE` | `sales_data` |

Example AWS Glue job arguments:

`--JOB_NAME aws-glue-sales-etl`

`--SOURCE_PATH s3://enterprise-etl-bucket/raw/sales_data/`

`--OUTPUT_PATH s3://enterprise-etl-bucket/processed/sales/`

`--SUMMARY_PATH s3://enterprise-etl-bucket/processed/regional_summary/`

`--GLUE_DATABASE enterprise_db`

`--GLUE_TABLE sales_data`

## AWS Glue Crawler

The crawler discovers the schema of the raw sales dataset and registers it in the Glue Data Catalog.

See `crawler_config.md` for the recommended crawler configuration.

Typical flow:

1. Upload raw CSV data to Amazon S3.
2. Create the Glue database.
3. Configure the Glue crawler.
4. Run the crawler.
5. Verify the `sales_data` catalog table.
6. Create the Glue ETL job.
7. Configure the job parameters.
8. Run the ETL job.
9. Verify the processed Parquet output in S3.

## Local Testing

AWS Glue's `awsglue` package is provided by the AWS Glue runtime and is not required for the local transformation test.

The reusable transformation logic is located in:

`transformations.py`

The local test uses:

`local_test.py`

Sample input data is located in:

`sample_data/sales_data.csv`

### Prerequisites

Install PySpark:

```text
pip install pyspark
```

Java 17 or a compatible Java runtime is recommended for the PySpark environment used by this project.

On Windows, Spark may require Hadoop native utilities such as `winutils.exe` for local filesystem operations.

### Run the Local Test

From the project directory:

```text
python local_test.py
```

The test:

- Reads the sample CSV dataset.
- Removes duplicates.
- Removes invalid records.
- Calculates transaction totals.
- Creates a regional sales summary.
- Writes detailed Parquet output.
- Writes summary Parquet output.

### Expected Local Test Result

The sample dataset contains 8 records.

After cleaning:

`5 valid records`

Expected regional sales:

| Region | Regional Sales |
|---|---:|
| East | 77400 |
| North | 5000 |
| South | 18000 |
| West | 4000 |

The local test creates:

```text
local_output/
+-- sales/
|   +-- region=East/
|   +-- region=North/
|   +-- region=South/
|   +-- region=West/
|
+-- regional_summary/
```

The `local_output/` directory is excluded from Git through `.gitignore`.

## Production Design Considerations

### IAM Security

AWS Glue should use an IAM execution role rather than hard-coded AWS credentials.

The role should follow the principle of least privilege and only access the required S3 locations and Glue resources.

### Data Lake Organization

A recommended S3 structure is:

```text
s3://enterprise-etl-bucket/
|
+-- raw/
|   +-- sales_data/
|
+-- processed/
    +-- sales/
    |   +-- region=East/
    |   +-- region=North/
    |   +-- region=South/
    |   +-- region=West/
    |
    +-- regional_summary/
```

### Parquet

Parquet is used for processed datasets because it is a columnar format that works efficiently with modern analytics engines.

### Partitioning

Detailed sales data is partitioned by `region`.

For larger production datasets, additional partitioning strategies can be evaluated based on query patterns, data volume, and partition cardinality.

### Job Bookmarks

AWS Glue job bookmarks can be enabled for incremental processing when the source data is continuously updated.

This prevents already-processed data from being unnecessarily processed again.

### Monitoring

Production deployments should integrate AWS Glue job monitoring with Amazon CloudWatch.

Recommended monitoring areas include:

- Job failures
- Job duration
- Input record counts
- Output record counts
- Data quality failures
- S3 output availability
- Crawler failures

## Error Handling

The Glue job validates required columns before processing.

If required columns are missing, the job raises an exception instead of silently producing incorrect output.

Unexpected ETL failures are logged with stack traces and cause the Glue job to fail, making failures visible to orchestration and monitoring systems.

## Reusable Transformation Layer

The transformation functions are intentionally separated from the AWS Glue runtime.

`transformations.py` contains reusable PySpark transformations:

- `clean_and_transform()`
- `build_regional_summary()`

This separation provides two benefits:

1. The same business logic can be tested locally.
2. The AWS Glue runtime-specific code remains isolated in `glue_job.py`.

This is a common pattern for making data engineering code easier to test and maintain.

## Files

### `glue_job.py`

Production AWS Glue ETL entry point.

Reads from the Glue Data Catalog and writes processed Parquet datasets to Amazon S3.

### `transformations.py`

Reusable PySpark transformation and aggregation logic.

### `local_test.py`

Local validation script that runs the transformation logic using standard PySpark.

### `sample_data/sales_data.csv`

Synthetic test data used for local validation.

### `crawler_config.md`

AWS Glue crawler configuration reference.

### `.gitignore`

Prevents local Spark output, Python cache files, and temporary files from being committed.

## Security

Never commit:

- AWS access keys
- AWS secret keys
- API keys
- Passwords
- Production credentials
- Cloud account secrets
- Production customer data
- Confidential datasets

Use IAM roles, AWS Secrets Manager, environment variables, or other approved secret-management mechanisms for production deployments.

The sample dataset included in this repository is synthetic.

## Book Reference

This repository is the companion implementation for:

**Advanced Data Engineering Projects with Python, SQL & Cloud**

The project demonstrates practical AWS Glue ETL concepts including:

- AWS Glue Data Catalog
- Glue Crawlers
- Glue ETL
- PySpark transformations
- Data validation
- S3 data lake processing
- Parquet
- Partitioning
- Aggregation
- Local testing
- Production-oriented data engineering practices

## License

This project is provided for educational and demonstration purposes.
