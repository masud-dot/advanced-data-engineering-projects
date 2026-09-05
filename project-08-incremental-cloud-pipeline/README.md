# Project 08 — Incremental Cloud Data Pipeline

A production-oriented demonstration of incremental data processing using watermarks, change detection, validation, Parquet output, and warehouse upsert patterns.

This project is part of the companion implementation for the book:

**Advanced Data Engineering Projects with Python, SQL & Cloud**

## 1. Project Overview

Large data platforms rarely need to process every source record during every pipeline run.

An incremental pipeline processes only records that are new or have changed since the previous successful run. This reduces processing time, cloud storage operations, compute consumption, and downstream load.

This project demonstrates a watermark-based incremental pipeline for customer transactions.

The pipeline:

1. Reads the last successful watermark.
2. Extracts records whose `updated_at` is newer than that watermark.
3. Cleans and transforms the incremental dataset.
4. Removes duplicate transaction records.
5. Validates the resulting data.
6. Writes the incremental result as Parquet.
7. Determines the maximum processed `updated_at`.
8. Advances the watermark only after the output step succeeds.
9. Provides SQL for loading/upserting the incremental data into a warehouse.

The local implementation uses CSV as the source and Parquet as the output. In a production AWS environment, the same pattern can be extended to Amazon S3 and a cloud data warehouse.

## 2. Business Scenario

Assume an organization receives customer transaction data continuously.

A source table contains transaction ID, customer ID, transaction amount, creation timestamp, and last update timestamp.

A naive batch pipeline might read the entire table every day. If only a small portion of records changed, reprocessing the entire dataset is inefficient.

An incremental pipeline instead stores a watermark:

```text
Previous watermark
        ↓
Extract records where updated_at > watermark
        ↓
Transform
        ↓
Validate
        ↓
Write output
        ↓
Advance watermark
```

This allows the pipeline to focus on the changed portion of the dataset.

## 3. Architecture

### Logical Architecture

```text
                 Source Database
                       |
                       v
              customer_transactions
                       |
                       v
              Watermark Metadata
                       |
                       v
             Incremental Extraction
                       |
                       v
                Data Cleaning
                       |
                       v
                 Deduplication
                       |
                       v
                  Validation
                       |
                       v
             Partitioned Parquet
                       |
              +--------+--------+
              |                 |
              v                 v
          Amazon S3       Warehouse Staging
                                |
                                v
                         MERGE / UPSERT
                                |
                                v
                       Analytics Warehouse
```

### Production Cloud Pattern

```text
Source DB
   |
   v
Incremental Extract
   |
   v
Amazon S3
   |
   v
Parquet Data Lake
   |
   v
ETL / Spark / Glue
   |
   v
Warehouse
   |
   v
Analytics
```

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Pipeline processing |
| Pandas | Local data transformation |
| SQLAlchemy | Database connectivity |
| PostgreSQL | Local relational demonstration |
| PyArrow | Parquet generation |
| SQL | Incremental extraction and warehouse operations |
| Amazon S3 | Production cloud storage pattern |
| pytest | Automated testing |

## 5. Project Structure

```text
project-08-incremental-cloud-pipeline/
├── README.md
├── .gitignore
├── pipeline.py
├── requirements.txt
├── sample_data/
│   └── source_data.csv
├── src/
│   ├── incremental_pipeline.py
│   ├── transformations.py
│   ├── validation.py
│   └── watermark.py
├── sql/
│   ├── schema.sql
│   ├── source_schema.sql
│   ├── target_schema.sql
│   ├── incremental_queries.sql
│   └── upsert.sql
└── tests/
    └── test_pipeline.py
```

## 6. Source Data

The sample dataset contains synthetic customer transactions.

The important field for incremental processing is:

```text
updated_at
```

It represents the latest known modification time for a transaction.

## 7. Source Schema

The source table is defined in `sql/source_schema.sql`.

```sql
CREATE TABLE customer_transactions (
    transaction_id BIGINT PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```

| Column | Description |
|---|---|
| transaction_id | Unique transaction identifier |
| customer_id | Customer associated with the transaction |
| amount | Transaction value |
| created_at | Original creation timestamp |
| updated_at | Most recent modification timestamp |

## 8. Watermark Strategy

A watermark represents the latest successfully processed timestamp.

The project stores it in `pipeline_metadata`.

```sql
CREATE TABLE pipeline_metadata (
    pipeline_name VARCHAR(100) PRIMARY KEY,
    last_watermark TIMESTAMP NOT NULL
);
```

Initial value:

```text
2026-01-01 00:00:00
```

The extraction condition is:

```sql
WHERE updated_at > :last_watermark
```

If the watermark is:

```text
2026-01-15 00:00:00
```

records updated after that timestamp are selected.

## 9. Why the Watermark Must Advance After Success

A critical design principle is:

> Never advance the watermark before the downstream operation succeeds.

The safe sequence is:

```text
Read watermark
     ↓
Extract
     ↓
Transform
     ↓
Validate
     ↓
Write output
     ↓
SUCCESS
     ↓
Advance watermark
```

If the output operation fails, the watermark remains unchanged. The next execution can retry those records.

## 10. Incremental Extraction

The reusable extraction function is implemented in `src/incremental_pipeline.py`.

The pipeline converts `updated_at` to a timestamp and applies the watermark condition.

Conceptually:

```python
result = df[
    df["updated_at"] > watermark_ts
]
```

The result is ordered by:

```text
updated_at
transaction_id
```

This provides deterministic processing order.

## 11. Data Transformation

The transformation layer is implemented in `src/transformations.py`.

The transformation process:

1. Converts transaction amounts to numeric values.
2. Converts timestamp fields to datetime values.
3. Removes records with invalid required fields.
4. Removes duplicate transaction IDs.
5. Adds partition columns.

The generated partition columns are:

```text
year
month
day
```

These fields can support partitioned cloud storage layouts.

## 12. Deduplication

Incremental systems may receive repeated versions of the same business record.

The project protects against duplicate transaction IDs using:

```python
result.drop_duplicates(
    subset=["transaction_id"],
    keep="last"
)
```

For a production CDC system, deduplication rules should be aligned with the source system's change semantics and event ordering guarantees.

## 13. Data Validation

Validation is implemented in `src/validation.py`.

The validation layer checks:

- Required columns
- Duplicate transaction IDs
- Negative transaction amounts
- Null `updated_at` values

Failing validation prevents invalid records from being silently propagated downstream.

## 14. Parquet Output

The local pipeline writes:

```text
incremental_output.parquet
```

using PyArrow.

Parquet is useful for analytical workloads because it is columnar, compact, efficient for analytical reads, and compatible with many data-engineering tools.

The generated Parquet file is intentionally excluded from Git through `.gitignore`.

## 15. Cloud Storage Pattern

In a production AWS implementation, the local Parquet output can be written to Amazon S3.

A recommended logical layout is:

```text
s3://<bucket>/incremental/customer_transactions/
    year=2026/
        month=1/
            day=20/
                data.parquet
```

Partitioning by date allows downstream analytical engines to scan only the required partitions.

The exact S3 bucket, IAM role, account ID, and credentials should be supplied through environment-specific configuration rather than committed to source control.

## 16. Warehouse Target

The target warehouse table is defined in `sql/target_schema.sql`.

```sql
CREATE TABLE warehouse_transactions (
    transaction_id BIGINT PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```

The transaction ID acts as the business key for the upsert.

## 17. Warehouse Upsert

The project includes an upsert pattern in `sql/upsert.sql`.

The incremental data is first staged and then applied to the warehouse.

```text
Incremental Parquet
       ↓
Staging Table
       ↓
UPSERT
       ↓
Warehouse Table
```

The PostgreSQL demonstration uses `ON CONFLICT`.

For warehouses that do not support PostgreSQL-style `ON CONFLICT`, the same business pattern can be implemented with `MERGE`.

## 18. Incremental SQL Queries

`sql/incremental_queries.sql` contains queries for:

- Incremental extraction
- Determining the next watermark
- Checking the current watermark
- Detecting duplicates
- Counting pending incremental rows

Example:

```sql
SELECT
    transaction_id,
    customer_id,
    amount,
    created_at,
    updated_at
FROM customer_transactions
WHERE updated_at > :last_watermark
ORDER BY updated_at, transaction_id;
```

## 19. Local Execution

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run:

```bash
python src/incremental_pipeline.py
```

The demonstration uses:

```text
2026-01-15 00:00:00
```

as the sample watermark.

The sample dataset contains five records after this point.

Expected result:

```text
Incremental rows processed: 5
```

The pipeline writes:

```text
incremental_output.parquet
```

## 20. Automated Tests

Run:

```bash
python -m pytest -q
```

The test suite covers:

1. Incremental filtering
2. Transformation and partition columns
3. Rejection of negative transaction amounts

Validated local result:

```text
3 passed
```

## 21. Python Syntax Validation

Run:

```bash
python -m py_compile pipeline.py src/*.py tests/test_pipeline.py
```

A successful command produces no error output.

## 22. Failure Handling

If extraction and transformation succeed but output fails, the watermark should not move.

On the next execution, the records can be retried.

Production implementations can add:

- Retry policies
- Dead-letter handling
- Transaction boundaries
- Job run identifiers
- Audit tables
- Structured logging
- Metrics
- Alerts
- Checkpointing

## 23. Idempotency

An incremental pipeline should ideally be safe to rerun.

This project supports that principle through:

- Watermark-based extraction
- Transaction-level deduplication
- Deterministic transformations
- Warehouse upsert logic
- Watermark advancement after successful output

## 24. Production Improvements

A production implementation could extend this project with:

### AWS S3

Replace local Parquet output with an S3 destination.

### AWS Glue

Use Glue for managed ETL processing.

### Apache Spark

Use Spark when the incremental dataset becomes too large for Pandas.

### Apache Airflow

Schedule and orchestrate the pipeline.

### AWS Lambda

Use event-driven execution for smaller workloads.

### CloudWatch

Monitor pipeline duration, records extracted, records rejected, records loaded, watermark progression, and failures.

### Data Quality Framework

Add checks for referential integrity, amount ranges, timestamp consistency, schema drift, and unexpected volume changes.

## 25. Watermark Limitations

A timestamp watermark is simple and useful, but it has limitations.

Potential problems include:

- Multiple records sharing the same timestamp
- Clock differences between systems
- Late-arriving data
- Updates after the watermark boundary
- Source timestamp precision limitations

For high-volume production systems, alternatives may include:

- Database log-based CDC
- Change Data Capture tools
- Sequence-based offsets
- Event IDs
- Composite watermarks
- Source-native change tracking

The appropriate strategy depends on the source system and its consistency guarantees.

## 26. Security

Never commit:

- Database passwords
- AWS access keys
- Secret keys
- API tokens
- Production credentials
- Real customer data
- Private certificates

Use environment variables or a secrets manager.

Example configuration names:

```text
DATABASE_URL
AWS_REGION
AWS_ROLE_ARN
S3_BUCKET
```

The repository uses synthetic data and placeholder cloud configuration.

## 27. Troubleshooting

### ModuleNotFoundError

Run the pipeline from the project root:

```bash
python src/incremental_pipeline.py
```

For tests:

```bash
python -m pytest -q
```

### No Incremental Records

Check the watermark.

If the watermark is greater than or equal to the maximum `updated_at`, there may be no new records.

### Parquet Error

Install:

```bash
python -m pip install pandas pyarrow
```

### Database Connection Error

Check:

```text
DATABASE_URL
PostgreSQL availability
Database name
Username
Password
Port
```

### Validation Failure

Inspect the data for missing required columns, null timestamps, negative amounts, or duplicate transaction IDs.

## 28. Local Testing vs Cloud Execution

The repository provides a locally testable implementation of the incremental processing logic.

The local demonstration uses:

```text
CSV → Pandas → Validation → Parquet
```

The production architecture extends this pattern to:

```text
Database → Incremental Extraction → S3 → ETL → Warehouse
```

The AWS infrastructure itself is not required to run the local tests and is not represented as a live deployment in this repository.

Local execution validates the Python processing logic. Deployment-specific behavior such as IAM permissions, S3 access, Glue execution, and warehouse connectivity must be validated in the target AWS environment.

## 29. File-by-File Guide

### `pipeline.py`

Database-oriented incremental pipeline entry point demonstrating database connection, watermark retrieval, incremental extraction, transformation, Parquet output, and watermark advancement.

### `src/incremental_pipeline.py`

Reusable local incremental processing implementation.

### `src/transformations.py`

Data cleaning, deduplication, timestamp conversion, and partition-column generation.

### `src/validation.py`

Business and structural data-quality validation.

### `src/watermark.py`

Utility for determining the next watermark.

### `sample_data/source_data.csv`

Synthetic source transaction data.

### `sql/schema.sql`

Local source and pipeline metadata schema.

### `sql/source_schema.sql`

Source table definition.

### `sql/target_schema.sql`

Warehouse target table definition.

### `sql/incremental_queries.sql`

Incremental extraction and monitoring queries.

### `sql/upsert.sql`

Warehouse upsert pattern.

### `tests/test_pipeline.py`

Automated tests for the local processing logic.

## 30. Learning Outcomes

After completing this project, a data engineer should understand:

- Why incremental processing is important
- How timestamp watermarks work
- How to extract only changed records
- How to handle duplicate records
- How to validate incremental datasets
- Why Parquet is useful in data lakes
- How partitioned cloud storage can improve analytics
- How staging and upsert patterns work
- Why watermark advancement must happen after successful processing
- How to design retry-friendly pipelines
- How local processing maps to a cloud architecture
- Where simple watermark approaches become insufficient
- How incremental pipelines fit into modern data platforms

## 31. Key Design Pattern

```text
              ┌────────────────────┐
              │  Previous          │
              │  Watermark         │
              └─────────┬──────────┘
                        │
                        v
              ┌────────────────────┐
              │ Incremental        │
              │ Extraction         │
              └─────────┬──────────┘
                        │
                        v
              ┌────────────────────┐
              │ Transform +        │
              │ Deduplicate        │
              └─────────┬──────────┘
                        │
                        v
              ┌────────────────────┐
              │ Validate           │
              └─────────┬──────────┘
                        │
                        v
              ┌────────────────────┐
              │ Write / Load       │
              └─────────┬──────────┘
                        │
                    SUCCESS
                        │
                        v
              ┌────────────────────┐
              │ Advance Watermark  │
              └────────────────────┘
```

This pattern is a foundational technique for efficient batch and cloud data pipelines.

## 32. Companion Repository

```text
https://github.com/masud-dot/advanced-data-engineering-projects
```

Project directory:

```text
project-08-incremental-cloud-pipeline
```

## 33. Book Reference

This implementation accompanies:

**Advanced Data Engineering Projects with Python, SQL & Cloud**

The repository provides practical code and supporting SQL for the project described in the book.

## 34. License

This project is provided for educational and demonstration purposes.

Use synthetic or appropriately authorized data when adapting the implementation for real systems.

Do not commit credentials, secrets, or confidential production data to source control.
