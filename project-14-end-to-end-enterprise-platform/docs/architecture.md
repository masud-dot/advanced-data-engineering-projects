# Enterprise Data Platform Architecture

## Overview

This project demonstrates an end-to-end enterprise data platform that integrates batch ingestion, data transformation, enrichment, lake storage, warehouse analytics, data quality, monitoring, and orchestration.

The architecture follows this flow:

```text
                    ┌─────────────────────┐
                    │     Data Sources     │
                    │ Customers / Products │
                    │       / Orders       │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │      Ingestion      │
                    │   Batch / Sources   │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │    Bronze Layer     │
                    │     Raw Parquet     │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │    Transformation   │
                    │ Clean / Standardize │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │     Enrichment      │
                    │ Customer / Product  │
                    │      Attributes     │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │     Silver Layer    │
                    │  Curated Parquet    │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Warehouse / Gold    │
                    │ Facts / Dimensions  │
                    │   Business Metrics  │
                    └──────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                 │
     ┌────────▼────────┐              ┌────────▼────────┐
     │  Data Quality   │              │   Monitoring     │
     │ Schema / Nulls  │              │ Runtime / Errors │
     │ Duplicates / FK │              │ Quality / Health │
     └────────┬────────┘              └────────┬────────┘
              │                                 │
              └────────────────┬────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │    Orchestration    │
                    │ Stages / Retry Flow │
                    └─────────────────────┘
```

## Architectural Layers

### 1. Source Layer

The sample platform consumes three business datasets:

- Customers
- Products
- Orders

In a production implementation, these sources could represent operational databases, SaaS applications, files, APIs, or event streams.

### 2. Ingestion Layer

`ingestion/source_ingestion.py` provides the source ingestion interface.

Responsibilities include:

- Loading source data
- Validating source availability
- Returning standardized datasets to downstream processing

### 3. Bronze Layer

The Bronze layer stores the ingested datasets in Parquet format.

Purpose:

- Preserve the ingested representation
- Provide a durable processing boundary
- Support repeatable downstream processing

### 4. Transformation Layer

`processing/transformation.py` standardizes the incoming datasets.

Examples include:

- Column-name normalization
- Type conversion
- Date parsing
- Duplicate removal
- Invalid revenue filtering
- Required-field cleanup

### 5. Enrichment Layer

`processing/enrichment.py` combines orders with customer and product attributes.

The resulting dataset provides a richer analytical representation of each order.

### 6. Silver Layer

The Silver layer stores transformed and enriched datasets.

This layer is intended to provide curated data suitable for analytical processing.

### 7. Warehouse / Gold Layer

`warehouse/analytics.py` produces warehouse-style datasets:

- `fact_orders`
- `dim_customer`
- `dim_product`
- `daily_sales`
- `product_performance`
- `customer_performance`

These datasets support business reporting and analytical workloads.

### 8. Data Quality

`quality/platform_quality.py` performs platform-level checks covering:

- Required schemas
- Completeness
- Duplicate order IDs
- Revenue validation
- Referential integrity
- Date validation

The current platform requires a minimum quality score of 95%.

### 9. Monitoring

`monitoring/platform_monitor.py` tracks:

- Pipeline runtime
- Input and output volume
- Error count
- Quality score
- Overall platform health

The monitoring layer produces a `HEALTHY` or `UNHEALTHY` status.

### 10. Orchestration

`orchestration/workflow.py` provides reusable stage orchestration with configurable retries and retry delays.

A failed stage can be retried before the workflow is marked as failed.

## Design Principles

The project demonstrates several enterprise data-engineering principles:

- Layered data architecture
- Separation of ingestion and transformation
- Reusable processing components
- Data-quality gates
- Operational monitoring
- Retry-based orchestration
- Analytics-ready Gold datasets
- Configuration-driven platform behavior
- Testable Python modules
- Clear separation between pipeline logic and entry points

## Production Evolution

A production deployment could replace the local implementations with cloud-native services such as:

- Object storage for the data lake
- Managed Spark for large-scale processing
- Kafka for real-time ingestion
- Airflow or another orchestrator
- Cloud data warehouses
- Centralized observability
- Enterprise data catalogs
- CI/CD and infrastructure-as-code

The local implementation intentionally keeps the architecture executable without requiring paid cloud infrastructure.
