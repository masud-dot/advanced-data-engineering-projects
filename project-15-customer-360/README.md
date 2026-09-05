# Customer 360 Unified Analytics Platform

A practical, end-to-end Customer 360 analytics platform built with Python, SQL, Pandas, Parquet, automated data-quality checks, monitoring, and a layered data-lake architecture.

The project demonstrates how multiple customer-related data sources can be ingested, standardized, enriched, unified into customer profiles, segmented, validated, stored, and exposed for analytics.

---

## Project Overview

Organizations often have customer information spread across multiple systems:

- Customer master data
- Orders and transactions
- Product information
- Customer activity and engagement data

A Customer 360 platform brings these sources together to create a unified view of each customer.

This project implements that workflow as a reproducible data-engineering solution:

```text
Customers ────────┐
Orders ───────────┤
Products ─────────┤
Activity ─────────┘
        │
        ▼
   Ingestion
        │
        ▼
 Standardization
        │
        ▼
Transaction Processing
        │
        ▼
 Customer Enrichment
        │
        ▼
 Customer 360 Profile
        │
        ├── Customer Metrics
        ├── Segmentation
        ├── Quality Validation
        ├── Monitoring
        │
        ▼
   Gold Analytics
        │
        ▼
 SQL Analytics / Warehouse
```

---

## Business Objective

The platform is designed to answer practical questions such as:

- Who are the highest-value customers?
- How much revenue has each customer generated?
- Which customers are loyal or active?
- Which customers may require retention attention?
- Which product categories generate the most revenue?
- How engaged are customers?
- How complete and reliable is the unified customer data?

The result is an analytics-ready customer profile that combines customer, transaction, product, and activity information.

---

## Key Features

### Multi-Source Ingestion

Loads four source datasets:

- `customers.csv`
- `orders.csv`
- `products.csv`
- `customer_activity.csv`

### Data Standardization

The processing layer:

- Normalizes column names
- Standardizes data types
- Removes duplicate customer records
- Removes duplicate order/activity records
- Filters invalid values

### Transaction Processing

Transactions are enriched with product information and calculated metrics including:

- Revenue
- Transaction month
- Customer transaction totals
- Order counts
- Unit counts

### Customer Enrichment

Customer profiles are enriched with:

- Activity metrics
- Preferred product category
- Purchase metrics
- Engagement information

### Customer 360 Profile

The unified profile includes:

- Customer identity
- Region
- Customer age
- Recency
- Purchase frequency
- Lifetime value
- Engagement score
- Customer status
- Profile completeness

### Customer Segmentation

Customers are classified into business-oriented segments such as:

- `PROSPECT`
- `VIP`
- `AT_RISK`
- `NEW_CUSTOMER`
- `LOYAL`
- `ENGAGED`
- `ACTIVE`

### Data Quality

The quality framework validates:

- Required fields
- Customer ID completeness
- Customer ID uniqueness
- Lifetime value
- Order counts
- Profile completeness
- Referential integrity

### Monitoring

The monitoring layer tracks:

- Runtime
- Input records
- Output profiles
- Quality score
- Pipeline status
- Runtime alerts
- Quality alerts

---

## Project Structure

```text
project-15-customer-360/
│
├── README.md
├── requirements.txt
├── Dockerfile
├── .gitignore
│
├── configs/
│   └── customer360.yaml
│
├── ingestion/
│   └── customer_ingestion.py
│
├── processing/
│   ├── customer_standardization.py
│   ├── transaction_processing.py
│   └── customer_enrichment.py
│
├── customer360/
│   ├── profile_builder.py
│   ├── segmentation.py
│   └── metrics.py
│
├── storage/
│   └── customer360_lake.py
│
├── warehouse/
│   └── customer_analytics.py
│
├── quality/
│   └── customer360_quality.py
│
├── monitoring/
│   └── customer360_monitor.py
│
├── orchestration/
│   └── workflow.py
│
├── pipelines/
│   └── customer360_pipeline.py
│
├── src/
│   └── customer360.py
│
├── tests/
│   ├── test_ingestion.py
│   ├── test_standardization.py
│   ├── test_processing.py
│   ├── test_customer360.py
│   ├── test_quality.py
│   └── test_pipeline.py
│
├── sample_data/
│   ├── customers.csv
│   ├── orders.csv
│   ├── products.csv
│   └── customer_activity.csv
│
├── sql/
│   └── customer360_analytics.sql
│
└── docs/
    ├── architecture.md
    └── operations.md
```

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Pipeline implementation |
| Pandas | Data processing |
| PyYAML | Configuration |
| PyArrow | Parquet storage |
| Pytest | Automated testing |
| SQL | Analytics |
| Parquet | Data-lake storage |
| Docker | Containerized execution |
| Git | Version control |

---

## Configuration

Main configuration:

```text
configs/customer360.yaml
```

The configuration defines:

- Project metadata
- Environment
- Source files
- Processing options
- Customer 360 features
- Storage layers
- Warehouse entities
- Quality thresholds
- Monitoring thresholds
- Retry settings
- Analytics limits

Example:

```yaml
customer360:
  lifetime_value_enabled: true
  activity_metrics_enabled: true
  segmentation_enabled: true
  preferred_category_enabled: true

quality:
  enabled: true
  minimum_score: 95

monitoring:
  enabled: true
  runtime_threshold_seconds: 60
  minimum_quality_score: 95
```

---

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
source .venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run the Pipeline

Execute the complete Customer 360 platform:

```bash
python -m src.customer360
```

The pipeline performs ingestion, transformation, profile construction, segmentation, quality validation, storage, analytics, and monitoring.

---

## Example Results

The sample datasets contain:

```text
Customers: 8
Orders: 24
Products: 8
Activities: 24
```

A successful execution produces results such as:

```text
CUSTOMER 360 SUMMARY

Customers:              8
Orders:                 24
Units:                  37
Total Revenue:          $11,560.00
Average Customer Value: $1,445.00
Average Order Value:    $476.88
Average Engagement:     3.25

QUALITY

Quality Score:           100.00%
Quality Status:          PASS

MONITORING

Input Records:           64
Output Profiles:         8
Pipeline Status:         SUCCESS
```

Example top customers include:

```text
Emma Davis       LOYAL
Bob Smith        LOYAL
Alice Johnson    LOYAL
David Brown      LOYAL
Carol Williams   LOYAL
```

The sample execution produced:

```text
LOYAL: 5 customers
ACTIVE: 3 customers
```

---

## Data Lake Architecture

The platform follows a layered storage model:

```text
Bronze
  │
  │ Raw / ingested data
  ▼
Silver
  │
  │ Cleaned / standardized data
  ▼
Customer 360
  │
  │ Unified customer profiles
  ▼
Gold
  │
  │ Analytics-ready datasets
  ▼
Warehouse / BI
```

### Bronze

Stores source-level datasets.

### Silver

Stores standardized and processed datasets.

### Gold

Stores analytics-ready customer and business datasets.

Typical Gold outputs include:

```text
customer_360_profile.parquet
dim_customer.parquet
fact_customer_transactions.parquet
revenue_by_region.parquet
revenue_by_category.parquet
segment_performance.parquet
top_customers.parquet
segment_summary.parquet
```

---

## Data Quality

The platform evaluates the reliability of the unified customer dataset.

Validation includes:

```text
Required fields
Customer ID completeness
Customer ID uniqueness
Lifetime value validation
Order count validation
Profile completeness
Referential integrity
```

Configured minimum quality score:

```text
95%
```

The sample pipeline currently achieves:

```text
100.00% PASS
```

---

## Monitoring

The monitoring layer evaluates:

```text
Runtime
Input records
Output profiles
Quality score
Pipeline status
```

The default runtime threshold is:

```text
60 seconds
```

The minimum acceptable quality score is:

```text
95%
```

---

## SQL Analytics

Business queries are available in:

```text
sql/customer360_analytics.sql
```

The SQL examples cover:

- Customer lifetime value
- Revenue by region
- Segment performance
- Product-category performance
- Top customers
- At-risk customers
- Highly engaged customers
- Recent transactions

---

## Testing

Run all automated tests:

```bash
python -m pytest -q
```

Current validation:

```text
8 passed
```

Run Python compilation validation:

```bash
python -m compileall -q .
```

Check for whitespace errors before committing:

```bash
git diff --check
```

---

## Docker

Build the Docker image:

```bash
docker build -t customer360-platform .
```

Run the container:

```bash
docker run --rm customer360-platform
```

Docker execution is intended to provide the same end-to-end pipeline behavior as the local Python execution.

---

## Documentation

Detailed documentation is available under:

```text
docs/
```

### Architecture

`docs/architecture.md`

Explains:

- Platform architecture
- Data layers
- Processing flow
- Customer 360 design
- Quality
- Monitoring
- Orchestration
- Production extensions

### Operations

`docs/operations.md`

Explains:

- Installation
- Pipeline execution
- Testing
- Data-quality validation
- Monitoring
- Docker execution
- Troubleshooting
- Operational workflow

---

## Learning Outcomes

This project demonstrates practical concepts used in modern data-engineering and analytics platforms:

- Multi-source data ingestion
- Data standardization
- Data transformation
- Customer identity integration
- Transaction processing
- Customer lifetime value
- Customer segmentation
- Data-lake architecture
- Gold-layer modeling
- Data-quality engineering
- Referential-integrity validation
- Pipeline monitoring
- Automated testing
- SQL analytics
- Dockerized data pipelines
- Enterprise-oriented architecture

---

## Production Extensions

A production implementation could extend this project with:

- AWS S3 or Azure Data Lake Storage
- Apache Spark
- Apache Airflow
- Apache Kafka
- Databricks
- Snowflake
- Amazon Redshift
- dbt
- Great Expectations
- Prometheus
- Grafana
- Centralized logging
- CI/CD
- Secrets management
- Data catalog and lineage
- Role-based access control
- Encryption
- Data-retention policies

The current implementation intentionally remains lightweight and reproducible while providing a foundation for these enterprise extensions.

---

## Project Validation

The current implementation has been validated with:

```text
End-to-end pipeline     PASS
Automated tests         8 passed
Python compilation      PASS
Data quality            100%
Pipeline status         SUCCESS
```

---

## License

This project is provided for educational and demonstration purposes.

---

## Author

Masud Mondal

GitHub:

https://github.com/masud-dot/advanced-data-engineering-projects

---

## Related Projects

This project is part of a broader practical data-engineering project series covering:

- ETL pipelines
- PySpark
- AWS data lakes
- Kafka
- Spark Streaming
- AWS Glue
- Redshift
- Incremental pipelines
- Data lakehouse architecture
- CI/CD
- Monitoring and alerting
- Data quality
- Pipeline performance optimization
- Enterprise data platforms
- Customer 360 analytics
