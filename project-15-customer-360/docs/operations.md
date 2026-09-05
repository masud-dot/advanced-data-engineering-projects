# Customer 360 Unified Analytics Platform — Operations Guide

## 1. Overview

This guide explains how to install, run, validate, monitor, and troubleshoot the Customer 360 Unified Analytics Platform.

The project is designed to run locally with Python and can also be executed through Docker.

---

## 2. Prerequisites

Install:

- Python 3.10 or later
- pip
- Docker Desktop (optional, for container execution)
- Git

Recommended environment:

```text
Python virtual environment
Pandas
PyYAML
Pytest
PyArrow
```

---

## 3. Project Installation

From the project root:

```bash
python -m venv .venv
```

Activate the environment on Windows:

```bash
source .venv/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 4. Source Data

The sample source datasets are located under:

```text
sample_data/
```

The platform expects:

```text
customers.csv
orders.csv
products.csv
customer_activity.csv
```

These files provide the source data used by the Customer 360 pipeline.

---

## 5. Configuration

Runtime configuration is maintained in:

```text
configs/customer360.yaml
```

Important configuration areas include:

- Ingestion
- Processing
- Customer 360 features
- Storage paths
- Warehouse settings
- Data-quality thresholds
- Monitoring thresholds
- Orchestration retries
- Analytics limits

---

## 6. Run the Customer 360 Pipeline

From the project root:

```bash
python -m src.customer360
```

The command executes the complete pipeline:

```text
Ingestion
    ↓
Standardization
    ↓
Transaction Processing
    ↓
Customer Enrichment
    ↓
Profile Building
    ↓
Segmentation
    ↓
Analytics
    ↓
Quality
    ↓
Storage
    ↓
Monitoring
```

A successful execution reports:

- Customer count
- Order count
- Unit count
- Total revenue
- Average customer value
- Average order value
- Engagement score
- VIP customers
- At-risk customers
- Quality score
- Pipeline runtime
- Pipeline status
- Top customers
- Segment summary

---

## 7. Run Automated Tests

Run the complete test suite:

```bash
python -m pytest -q
```

The project contains tests covering:

- Ingestion
- Standardization
- Transaction processing
- Customer 360 profile construction
- Segmentation
- Data quality
- End-to-end pipeline execution

A successful validation currently produces:

```text
8 passed
```

---

## 8. Python Compilation Validation

Check the complete project for syntax errors:

```bash
python -m compileall -q .
```

No output indicates successful compilation.

---

## 9. Data Lake Outputs

The pipeline creates three logical storage layers:

```text
customer360_lake/
├── bronze/
├── silver/
└── gold/
```

### Bronze

Contains ingested source datasets.

### Silver

Contains standardized and cleaned datasets.

### Gold

Contains analytics-ready datasets including:

- `customer_360_profile.parquet`
- `dim_customer.parquet`
- `fact_customer_transactions.parquet`
- `revenue_by_region.parquet`
- `revenue_by_category.parquet`
- `segment_performance.parquet`
- `top_customers.parquet`
- `segment_summary.parquet`

---

## 10. Data Quality Operations

The quality layer validates:

- Required columns
- Customer ID completeness
- Customer ID uniqueness
- Non-negative lifetime value
- Non-negative order counts
- Non-empty profiles
- Referential integrity

The configured minimum quality score is 95%.

The pipeline reports:

```text
PASS
```

when the quality threshold is satisfied.

---

## 11. Monitoring Operations

The monitoring layer records:

- Runtime
- Input records
- Output profiles
- Quality score
- Pipeline status
- Runtime alerts
- Quality alerts

Default thresholds include:

```text
Runtime threshold: 60 seconds
Minimum quality score: 95%
```

The pipeline reports `SUCCESS` when no monitoring alerts are triggered.

---

## 12. Docker Execution

Build the image:

```bash
docker build -t customer360-platform .
```

Run the platform:

```bash
docker run --rm customer360-platform
```

The container should execute the same Customer 360 pipeline as the local Python command.

---

## 13. SQL Analytics

Business analytics examples are stored in:

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

The SQL assumes the Gold datasets are exposed as warehouse tables or views.

---

## 14. Troubleshooting

### Missing source file

If the pipeline reports:

```text
Source file not found
```

verify that all required CSV files exist under:

```text
sample_data/
```

### Dependency error

Reinstall the project dependencies:

```bash
pip install -r requirements.txt
```

### Test discovery issue

Run tests from the project root:

```bash
python -m pytest -q
```

Make sure the `tests/` directory contains the test files.

### Parquet-related error

The storage layer uses Parquet. Install PyArrow:

```bash
pip install pyarrow
```

### Docker build failure

Check Docker Desktop is running and rebuild:

```bash
docker build -t customer360-platform .
```

### Quality failure

Inspect the quality result printed by the pipeline.

Common causes include:

- Duplicate customer IDs
- Missing customer IDs
- Negative revenue
- Invalid order counts
- Invalid customer references

---

## 15. Operational Checklist

Before considering a deployment successful, verify:

```text
[ ] Source datasets available
[ ] Dependencies installed
[ ] Configuration available
[ ] Pipeline executes successfully
[ ] Automated tests pass
[ ] Python compilation passes
[ ] Data-quality score meets threshold
[ ] Referential integrity passes
[ ] Gold datasets are generated
[ ] Monitoring reports SUCCESS
[ ] Docker build succeeds
[ ] Docker execution succeeds
```

---

## 16. Production Considerations

For production deployment, consider adding:

- Cloud object storage
- Managed data warehouse
- Apache Airflow
- Apache Spark
- Apache Kafka
- dbt
- Great Expectations
- Prometheus and Grafana
- Centralized logging
- CI/CD pipelines
- Secrets management
- Data catalog and lineage
- Access control and encryption
- Automated data-retention policies

The current project provides a local, reproducible implementation that can serve as a foundation for these production extensions.

---

## 17. Recommended Operational Workflow

A practical operating sequence is:

```text
1. Validate source files
        ↓
2. Review configuration
        ↓
3. Run automated tests
        ↓
4. Execute Customer 360 pipeline
        ↓
5. Review quality score
        ↓
6. Review monitoring results
        ↓
7. Validate Gold datasets
        ↓
8. Review SQL analytics
        ↓
9. Run Docker validation
```

This workflow helps catch data, code, quality, and deployment issues before the platform is promoted to a production environment.
