# Project 09 --- Data Lakehouse Architecture

A practical Bronze--Silver--Gold data lakehouse implementation using
Python, Parquet, Apache Spark concepts, Amazon S3, and Amazon Athena.

This project demonstrates how raw transactional data can move through a
modern lakehouse architecture from ingestion to analytics-ready
datasets.

> **Companion project:** This repository is part of the practical
> implementations for *Advanced Data Engineering Projects with Python,
> SQL & Cloud*.

------------------------------------------------------------------------

## 1. Project Overview

Traditional data warehouses often require data to be heavily structured
before it can be stored and analyzed. A data lake provides flexible
storage for raw data but can become difficult to manage when quality,
governance, and business meaning are not controlled.

A **data lakehouse** combines the flexible storage model of a data lake
with the organization and analytical capabilities associated with a
warehouse.

This project implements a simplified **Medallion Architecture**:

``` text
                 Raw Source Data
                       |
                       v
              +------------------+
              |      BRONZE      |
              | Raw / Immutable  |
              | Parquet Storage  |
              +------------------+
                       |
                       v
              +------------------+
              |      SILVER      |
              | Cleaned / Valid  |
              | Deduplicated     |
              +------------------+
                       |
                       v
              +------------------+
              |       GOLD       |
              | Business Metrics |
              | Analytics Ready  |
              +------------------+
                       |
                       v
                Amazon Athena
```

The local implementation uses Pandas and Parquet so the project can be
executed without an AWS account. The repository also contains Spark, S3,
and Athena patterns for production-oriented deployment.

------------------------------------------------------------------------

## 2. Business Scenario

Assume an organization receives sales transactions from multiple
operational systems.

Each transaction contains:

-   Transaction ID
-   Customer ID
-   Product ID
-   Transaction amount
-   Event timestamp
-   Region

The data engineering platform must:

1.  Receive raw transaction data.
2.  Preserve the source records.
3.  Clean invalid records.
4.  Remove duplicate transactions.
5.  Validate business rules.
6.  Store analytics-ready data.
7.  Produce product-level sales metrics.
8.  Make the curated data queryable through SQL.

The lakehouse architecture separates these responsibilities into
distinct layers.

------------------------------------------------------------------------

## 3. Technology Stack

  Technology      Purpose
  --------------- -------------------------------------------------
  Python          Pipeline orchestration and local processing
  Pandas          Local transformation and validation
  Apache Spark    Production-scale distributed processing pattern
  Parquet         Columnar analytical storage
  Amazon S3       Cloud object storage
  Amazon Athena   Serverless SQL analytics
  PyTest          Automated testing
  SQL             Schema and analytics definitions

------------------------------------------------------------------------

## 4. Repository Structure

``` text
project-09-data-lakehouse/
│
├── README.md
├── .gitignore
├── pipeline.py
├── bronze.py
├── silver.py
├── gold.py
├── quality.py
├── requirements.txt
│
├── sample_data/
│   └── raw_sales.csv
│
├── src/
│   ├── lakehouse_pipeline.py
│   ├── transformations.py
│   └── validation.py
│
├── sql/
│   ├── bronze_schema.sql
│   ├── silver_schema.sql
│   ├── gold_schema.sql
│   ├── analytics.sql
│   └── athena.sql
│
└── tests/
    └── test_lakehouse.py
```

------------------------------------------------------------------------

# 5. Medallion Architecture

## 5.1 Bronze Layer

The Bronze layer is the landing layer.

Its primary responsibility is to preserve incoming data with minimal
transformation.

Example production pattern:

``` python
spark.read.json("s3://raw-transactions/")
```

The data is then stored as Parquet:

``` python
raw_df.write \
    .mode("append") \
    .partitionBy("year", "month", "day") \
    .parquet("s3://enterprise-lakehouse/bronze/")
```

### Bronze principles

-   Preserve source information.
-   Avoid destructive transformations.
-   Maintain ingestion history where appropriate.
-   Use scalable object storage.
-   Partition data when access patterns justify it.
-   Keep the layer suitable for replay and reprocessing.

The local project writes the Bronze dataset to:

``` text
local_output/bronze/sales.parquet
```

------------------------------------------------------------------------

# 6. Silver Layer

The Silver layer converts raw records into trustworthy analytical data.

The project performs:

-   Data type conversion.
-   Timestamp parsing.
-   Null handling.
-   Positive-amount validation.
-   Duplicate transaction removal.
-   Region cleanup.
-   Date enrichment.

Example transformation:

``` python
result["amount"] = pd.to_numeric(
    result["amount"],
    errors="coerce",
)

result["event_time"] = pd.to_datetime(
    result["event_time"],
    errors="coerce",
)
```

Invalid records are removed before validation:

``` python
result = result[result["amount"] > 0]
```

Duplicate transactions are handled using the business key:

``` python
result = result.drop_duplicates(
    subset=["transaction_id"],
    keep="last",
)
```

Date attributes are added for analytical partitioning and filtering:

``` text
year
month
day
```

The local Silver output is:

``` text
local_output/silver/sales.parquet
```

------------------------------------------------------------------------

# 7. Gold Layer

The Gold layer contains business-ready datasets.

This project creates product-level sales metrics:

-   Total sales
-   Order count
-   Average order value

The transformation is:

``` python
gold = (
    df.groupby("product_id", as_index=False)
    .agg(
        total_sales=("amount", "sum"),
        order_count=("transaction_id", "count"),
        avg_order_value=("amount", "mean"),
    )
    .sort_values("total_sales", ascending=False)
)
```

The resulting dataset is written to:

``` text
local_output/gold/gold_sales.parquet
```

Gold datasets should be designed around business questions rather than
simply mirroring source tables.

------------------------------------------------------------------------

# 8. Sample Dataset

The repository contains synthetic sales transactions in:

``` text
sample_data/raw_sales.csv
```

The sample contains 15 transactions across four products:

``` text
P100
P200
P300
P400
```

The data spans January 2026 and contains multiple regions and customers.

No production or personally identifiable data is included.

------------------------------------------------------------------------

# 9. Local Execution

## 9.1 Create a Virtual Environment

Windows Git Bash:

``` bash
python -m venv .venv
source .venv/Scripts/activate
```

Linux/macOS:

``` bash
python -m venv .venv
source .venv/bin/activate
```

## 9.2 Install Dependencies

``` bash
pip install -r requirements.txt
```

## 9.3 Run the Pipeline

``` bash
python pipeline.py
```

Expected output includes:

``` text
Bronze rows: 15
Silver rows: 15
Gold rows: 4
```

The pipeline creates:

``` text
local_output/
├── bronze/
│   └── sales.parquet
├── silver/
│   └── sales.parquet
└── gold/
    └── gold_sales.parquet
```

------------------------------------------------------------------------

# 10. Data Quality Validation

The Silver layer is validated before Gold aggregation.

The project checks:

-   Required columns.
-   Duplicate transaction IDs.
-   Null amounts.
-   Non-positive amounts.
-   Null event timestamps.
-   Null customer IDs.
-   Null product IDs.

Run the quality checks independently:

``` bash
python quality.py
```

Expected result:

``` text
All Silver quality checks passed.
Validated rows: 15
```

This separation between transformation and validation makes failures
easier to diagnose.

------------------------------------------------------------------------

# 11. Automated Tests

The project includes PyTest tests covering:

1.  Silver transformation.
2.  Data quality rejection.
3.  Gold aggregation.

Run:

``` bash
python -m pytest -q
```

Expected result:

``` text
3 passed
```

The tests intentionally verify both successful processing and rejection
of invalid business data.

------------------------------------------------------------------------

# 12. SQL Layer

The `sql/` directory contains SQL definitions for the cloud
architecture.

## Bronze

`bronze_schema.sql` defines an external Parquet table pointing to the
Bronze S3 location.

``` text
s3://enterprise-lakehouse/bronze/
```

## Silver

`silver_schema.sql` defines the curated Silver dataset:

``` text
s3://enterprise-lakehouse/silver/
```

## Gold

`gold_schema.sql` defines the business-ready Gold dataset:

``` text
s3://enterprise-lakehouse/gold/
```

The schemas are written as external-table patterns suitable for query
engines such as Amazon Athena.

------------------------------------------------------------------------

# 13. Amazon S3 Lakehouse Layout

A production-oriented S3 layout can look like:

``` text
s3://enterprise-lakehouse/

├── bronze/
│   └── year=2026/
│       └── month=01/
│           └── day=24/
│
├── silver/
│   └── year=2026/
│       └── month=01/
│
└── gold/
    └── sales/
```

The exact partition strategy should be based on query patterns and data
volume.

Partitioning everything by every possible column is not automatically
better. Excessive partitioning can create many small files and increase
operational overhead.

------------------------------------------------------------------------

# 14. Amazon Athena

Athena can query the curated Parquet datasets directly from S3.

Example:

``` sql
SELECT
    product_id,
    total_sales AS revenue,
    order_count AS orders,
    avg_order_value AS avg_value
FROM gold_sales
ORDER BY revenue DESC
LIMIT 20;
```

Additional examples are available in:

``` text
sql/athena.sql
```

Athena is particularly useful when the organization wants serverless SQL
access without maintaining a traditional database server.

------------------------------------------------------------------------

# 15. Example Analytics

The Gold layer can answer questions such as:

### Which products generate the most revenue?

``` sql
SELECT
    product_id,
    total_sales
FROM gold_sales
ORDER BY total_sales DESC;
```

### Which regions generate the most revenue?

``` sql
SELECT
    region,
    SUM(amount) AS revenue
FROM silver_sales
GROUP BY region
ORDER BY revenue DESC;
```

### How does revenue change by month?

``` sql
SELECT
    year,
    month,
    SUM(amount) AS revenue
FROM silver_sales
GROUP BY year, month
ORDER BY year, month;
```

These queries demonstrate the separation between engineering datasets
and business-facing analytics.

------------------------------------------------------------------------

# 16. Spark Production Pattern

The local implementation uses Pandas because it is easy to execute on a
developer machine.

For larger datasets, the same architecture can be implemented with
Apache Spark.

Conceptually:

``` text
S3 Raw JSON
     |
     v
Spark DataFrame
     |
     v
Bronze Parquet
     |
     v
Spark Cleaning
     |
     v
Silver Parquet
     |
     v
Spark Aggregation
     |
     v
Gold Parquet
     |
     v
Athena
```

The repository's `bronze.py`, `silver.py`, and `gold.py` document the
corresponding Spark-layer responsibilities.

A real deployment would normally create and configure a Spark session
explicitly and supply cloud-specific configuration through the execution
environment.

------------------------------------------------------------------------

# 17. Why Parquet?

Parquet is a columnar storage format widely used in analytical data
platforms.

Advantages include:

-   Column pruning.
-   Compression.
-   Efficient analytical scans.
-   Good interoperability.
-   Strong integration with Spark.
-   Native support in many cloud analytics services.

For example, a query that needs only:

``` text
product_id
amount
```

does not necessarily need to scan every unrelated column in a Parquet
dataset.

------------------------------------------------------------------------

# 18. Partitioning Strategy

Partitioning can improve performance when queries frequently filter on
the partition columns.

This project demonstrates date-based partitioning:

``` text
year
month
day
```

A typical Bronze layout could therefore be:

``` text
bronze/
  year=2026/
    month=01/
      day=24/
```

Silver may use a coarser partition:

``` text
silver/
  year=2026/
    month=01/
```

Gold datasets may use a business-oriented organization instead of date
partitioning, depending on query patterns.

### Important consideration

Partitioning should not be applied blindly.

Too many tiny partitions can create:

-   Small-file problems.
-   Metadata overhead.
-   Slower query planning.
-   Higher operational complexity.

The correct strategy depends on data volume, access patterns, and file
sizes.

------------------------------------------------------------------------

# 19. Data Quality Architecture

A production lakehouse should treat quality as a first-class pipeline
capability.

A useful flow is:

``` text
Raw Data
   |
   v
Bronze
   |
   v
Transformation
   |
   +----> Quality Failure ----> Quarantine / Alert
   |
   v
Silver
   |
   v
Gold
```

Typical production checks include:

-   Schema validation.
-   Null checks.
-   Uniqueness.
-   Referential integrity.
-   Range checks.
-   Freshness.
-   Record counts.
-   Duplicate detection.
-   Business-rule validation.

This project implements a representative subset locally.

------------------------------------------------------------------------

# 20. Idempotency and Reprocessing

Production lakehouse pipelines should be designed so that retries do not
corrupt downstream data.

Important techniques include:

-   Stable business keys.
-   Deterministic transformations.
-   Controlled write modes.
-   Deduplication.
-   Checkpointing where applicable.
-   Partition-aware processing.
-   Transactional table formats where required.

This project demonstrates deduplication using:

``` text
transaction_id
```

For more advanced implementations, formats such as Apache Iceberg, Delta
Lake, or Apache Hudi can provide additional table-management
capabilities.

------------------------------------------------------------------------

# 21. Local vs Cloud Implementation

The local implementation is deliberately designed to run without AWS
credentials.

  Capability    Local Project       Production Pattern
  ------------- ------------------- ----------------------------------
  Storage       Local filesystem    Amazon S3
  Processing    Pandas              Apache Spark
  Format        Parquet             Parquet / Lakehouse table format
  SQL           SQL definitions     Amazon Athena
  Data          Synthetic CSV       Enterprise sources
  Testing       PyTest              CI/CD + integration tests
  Credentials   None required       IAM roles / managed identity
  Scale         Developer machine   Distributed infrastructure

This distinction is important: successful local execution does not mean
that an AWS deployment has been executed.

------------------------------------------------------------------------

# 22. Security

Never place secrets directly in source code.

Do not commit:

``` text
AWS access keys
AWS secret keys
Database passwords
API tokens
Private certificates
Production datasets
```

Production deployments should use:

-   IAM roles.
-   Least-privilege permissions.
-   AWS Secrets Manager where secrets are required.
-   Encryption at rest.
-   Encryption in transit.
-   S3 bucket policies.
-   CloudTrail and audit logging.
-   Environment-specific configuration.

The repository uses only synthetic data and contains no production
credentials.

------------------------------------------------------------------------

# 23. Monitoring and Operational Considerations

A production implementation should monitor:

### Pipeline health

-   Job success/failure.
-   Runtime.
-   Retry count.
-   Dependency failures.

### Data health

-   Input record count.
-   Output record count.
-   Rejected records.
-   Duplicate records.
-   Null rates.
-   Freshness.

### Storage health

-   File counts.
-   Small-file growth.
-   Partition growth.
-   Storage consumption.

### Query health

-   Athena scan volume.
-   Query duration.
-   Failed queries.
-   Frequently accessed datasets.

A mature lakehouse treats observability as part of the data platform
rather than an afterthought.

------------------------------------------------------------------------

# 24. CI/CD Recommendations

The repository is suitable for integration into a CI pipeline.

A basic CI process can:

``` text
Git Push
   |
   v
Install Dependencies
   |
   v
Run PyTest
   |
   v
Run Python Compilation
   |
   v
Validate SQL / Repository
   |
   v
Build / Deploy
```

Useful checks include:

``` bash
python -m pytest -q
python -m py_compile pipeline.py bronze.py silver.py gold.py quality.py src/*.py tests/test_lakehouse.py
```

Infrastructure deployment should be separated from application testing
where appropriate.

------------------------------------------------------------------------

# 25. Troubleshooting

## `ModuleNotFoundError`

Activate the virtual environment and install requirements:

``` bash
pip install -r requirements.txt
```

## Parquet engine error

Install PyArrow:

``` bash
pip install pyarrow
```

## PyTest not found

Install:

``` bash
pip install pytest
```

## AWS access errors

The local implementation does not require AWS credentials.

AWS errors only apply when adapting the project to a real
S3/Athena/Spark environment.

## Spark startup problems

Check:

-   Java installation.
-   `JAVA_HOME`.
-   Spark version compatibility.
-   Hadoop/S3 connector configuration.
-   Cloud IAM permissions.

------------------------------------------------------------------------

# 26. Limitations

This repository is a practical demonstration rather than a complete
production cloud platform.

The local pipeline:

-   Does not require AWS.
-   Does not execute against live S3.
-   Does not execute against live Athena.
-   Does not create a managed Spark cluster.
-   Uses Pandas for local processing.
-   Uses Parquet files rather than a transactional lakehouse table
    format.

The Spark and cloud examples illustrate the architecture and
implementation approach.

For enterprise deployments, additional components may be required for:

-   Workflow orchestration.
-   Catalog management.
-   Schema evolution.
-   Transaction management.
-   Data lineage.
-   Security governance.
-   Monitoring.
-   Cost management.
-   Disaster recovery.

------------------------------------------------------------------------

# 27. Project Validation

The implementation was validated locally with:

``` text
PyTest: 3 passed
Python compilation: Passed
Bronze output: Generated
Silver output: Generated
Gold output: Generated
Data quality checks: Passed
```

Sample pipeline result:

``` text
Bronze rows: 15
Silver rows: 15
Gold rows: 4
```

The four Gold product aggregates demonstrate the complete local flow
from source data through the three lakehouse layers.

------------------------------------------------------------------------

# 28. Learning Outcomes

After completing this project, a data engineer should understand:

-   What a data lakehouse is.
-   Why Medallion Architecture is useful.
-   How Bronze, Silver, and Gold layers differ.
-   How raw data can be preserved before transformation.
-   How to clean and validate analytical data.
-   How Parquet supports analytical workloads.
-   How partitioning affects lakehouse performance.
-   How S3 can provide scalable lake storage.
-   How Spark can scale transformation workloads.
-   How Athena can query S3-based datasets.
-   Why data quality must be integrated into pipelines.
-   Why local validation and cloud deployment are separate concerns.
-   How to structure a maintainable data engineering project.

------------------------------------------------------------------------

# 29. Recommended Production Evolution

A natural progression from this project is:

``` text
Local Pandas Pipeline
        |
        v
PySpark Processing
        |
        v
Amazon S3
        |
        v
Glue / Spark / Databricks
        |
        v
Iceberg / Delta Lake / Hudi
        |
        v
Athena / Warehouse / BI
        |
        v
Monitoring + Governance
```

This progression demonstrates how a small learning project can evolve
into an enterprise data platform.

------------------------------------------------------------------------

# 30. Final Takeaway

The most important lesson is that a lakehouse is not simply a folder
containing Parquet files.

A well-designed lakehouse establishes clear responsibilities:

``` text
Bronze = Preserve
Silver = Trust
Gold   = Serve
```

Bronze protects the raw data.

Silver creates reliable, validated datasets.

Gold presents business-ready information.

Together, these layers create a foundation for scalable analytics while
keeping data processing understandable, testable, and maintainable.

------------------------------------------------------------------------

## License / Usage

This repository is intended as a learning and companion implementation
for the book project.

Use synthetic or appropriately authorized data when adapting the
examples to real environments.

Never commit credentials, secrets, or confidential enterprise data.
