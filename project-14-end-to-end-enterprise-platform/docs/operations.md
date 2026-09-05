# Enterprise Data Platform Operations Guide

## Overview

This document explains how to run, validate, monitor, troubleshoot, and operate the End-to-End Enterprise Data Platform locally.

The project is designed to demonstrate enterprise data-engineering practices without requiring paid cloud infrastructure.

## Platform Workflow

The complete pipeline follows these stages:

1. Source ingestion
2. Bronze storage
3. Data transformation
4. Data enrichment
5. Silver storage
6. Warehouse-style dataset construction
7. Gold storage
8. Data-quality validation
9. Monitoring and health evaluation

The main executable entry point is:

```text
src/enterprise_platform.py
```

## Prerequisites

Recommended environment:

- Python 3.10 or newer
- pip
- Git
- Docker Desktop (optional)

The platform runs locally and does not require an AWS, Azure, or GCP account.

## Installation

From the project root, create and activate a virtual environment if desired:

```bash
python -m venv .venv
```

Windows Git Bash:

```bash
source .venv/Scripts/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Platform settings are maintained in:

```text
configs/platform.yaml
```

Important configuration areas include:

- Source files
- Processing mode
- Data lake paths
- Warehouse dataset names
- Minimum quality score
- Runtime threshold
- Monitoring settings
- Orchestration retry settings
- Analytics window

The current local implementation uses the project defaults defined by the Python components. The YAML file documents the intended platform configuration and provides a clear path toward configuration-driven production deployment.

## Running the Platform

Run the complete platform with:

```bash
python -m src.enterprise_platform
```

A successful run should display information similar to:

```text
Enterprise Data Platform
========================
Status: SUCCESS
Quality Score: 100.0%
Orders: 10
Customers: 5
Products: 5
Runtime: <runtime> seconds
Report: data_lake\platform_run_report.json
```

The exact runtime may vary depending on the machine and environment.

## Output Structure

After a successful execution, the platform creates:

```text
data_lake/
├── bronze/
│   ├── customers.parquet
│   ├── orders.parquet
│   └── products.parquet
├── silver/
│   ├── customers.parquet
│   ├── orders.parquet
│   └── products.parquet
├── gold/
│   ├── fact_orders.parquet
│   ├── dim_customer.parquet
│   ├── dim_product.parquet
│   ├── daily_sales.parquet
│   ├── product_performance.parquet
│   └── customer_performance.parquet
└── platform_run_report.json
```

The generated report provides a machine-readable summary of the pipeline execution.

## Data Quality Operations

The platform performs quality checks covering:

- Required schema fields
- Completeness
- Duplicate order IDs
- Revenue validation
- Referential integrity
- Date validation

The configured minimum quality score is 95%.

A score below the configured threshold results in an unhealthy platform status.

The quality implementation is located at:

```text
quality/platform_quality.py
```

## Monitoring Operations

The monitoring component tracks:

- Pipeline runtime
- Input row count
- Output row count
- Error count
- Quality score
- Runtime health
- Quality health
- Error health
- Overall platform health

Implementation:

```text
monitoring/platform_monitor.py
```

The final status is:

- `HEALTHY` when all configured health conditions pass
- `UNHEALTHY` when one or more conditions fail

## Orchestration and Retries

The reusable workflow component is located at:

```text
orchestration/workflow.py
```

It supports:

- Named pipeline stages
- Configurable retries
- Retry delays
- Stage-level success/failure results
- Early workflow termination after repeated failure

The default configuration allows up to three retries with a five-second delay between attempts.

## Testing

Run the complete automated test suite:

```bash
python -m pytest -q
```

The test suite covers the major platform components, including:

- Ingestion
- Transformation
- Storage
- Warehouse analytics
- Data quality
- End-to-end pipeline execution

For syntax validation:

```bash
python -m compileall -q .
```

For whitespace and patch validation:

```bash
git diff --check
```

## Docker Operations

The project includes a Dockerfile for containerized execution.

Build the image:

```bash
docker build -t enterprise-data-platform .
```

Run the container:

```bash
docker run --rm enterprise-data-platform
```

The container executes the same enterprise platform entry point used for local validation.

## Troubleshooting

### Source file not found

If ingestion reports a missing source file, verify that these files exist:

```text
sample_data/customers.csv
sample_data/products.csv
sample_data/orders.csv
```

Run from the project root so the relative paths resolve correctly.

### Dependency errors

Reinstall the project dependencies:

```bash
pip install -r requirements.txt
```

If a virtual environment is being used, verify that it is activated.

### Parquet errors

The project uses Parquet for Bronze, Silver, and Gold storage. Ensure the Parquet engine dependency listed in `requirements.txt` is installed correctly.

### Quality score below threshold

Inspect the quality result in:

```text
data_lake/platform_run_report.json
```

Review the individual checks to determine whether the problem is caused by:

- Missing required fields
- Null values
- Duplicate IDs
- Negative revenue
- Invalid customer references
- Invalid product references
- Invalid dates

### Pipeline reports UNHEALTHY

Check the monitoring section of:

```text
data_lake/platform_run_report.json
```

The report identifies whether the issue is related to:

- Runtime
- Data quality
- Pipeline errors

## Operational Validation Checklist

Before considering a local run successful, verify:

- [ ] Source CSV files are present
- [ ] Dependencies are installed
- [ ] Pipeline starts successfully
- [ ] Bronze datasets are created
- [ ] Silver datasets are created
- [ ] Gold datasets are created
- [ ] Quality score meets the minimum threshold
- [ ] No pipeline errors are reported
- [ ] Monitoring status is `HEALTHY`
- [ ] Execution report is generated
- [ ] Automated tests pass

## Recommended Production Operations

A production deployment would normally add:

- Centralized logging
- Cloud object storage
- Managed compute
- Production orchestration
- Secrets management
- Data cataloging
- Alert routing
- SLA and SLO monitoring
- CI/CD pipelines
- Infrastructure-as-code
- Environment-specific configuration
- Data retention policies
- Access control and audit logging

The local project intentionally keeps these dependencies lightweight while preserving the architecture and operational concepts.

## Operational Design Principles

The platform follows several operational principles:

1. **Fail visibly** — errors and quality failures should be observable.
2. **Validate early** — data-quality checks should prevent unreliable analytical output.
3. **Separate layers** — Bronze, Silver, and Gold provide clear processing boundaries.
4. **Measure execution** — runtime and volume metrics support operational analysis.
5. **Automate testing** — repeatable tests protect the pipeline from regressions.
6. **Support retries** — transient stage failures can be retried through the orchestration layer.
7. **Keep local execution reproducible** — the project can be validated without paid cloud services.

## Summary

This operations guide provides the procedures needed to install, execute, validate, monitor, troubleshoot, and containerize the enterprise data platform.

The same operating model can be extended toward cloud-based enterprise deployments while keeping the core separation between ingestion, processing, storage, analytics, quality, monitoring, and orchestration.
