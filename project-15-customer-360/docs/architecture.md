# Customer 360 Unified Analytics Platform — Architecture

## 1. Overview

The Customer 360 Unified Analytics Platform combines customer, transaction, product, and activity data into a single analytics-ready customer profile.

The platform follows a layered data engineering architecture:

```text
Customers ────────┐
Orders ───────────┤
Products ─────────┼──> Ingestion
Activity ─────────┘
                       │
                       ▼
                Standardization
                       │
                       ▼
              Transaction Processing
                       │
                       ▼
                 Enrichment
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
      Customer Metrics      Activity Metrics
             │                   │
             └─────────┬─────────┘
                       ▼
              Customer 360 Profile
                       │
                       ▼
                  Segmentation
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
          Analytics          Data Quality
             │                   │
             └─────────┬─────────┘
                       ▼
                Gold Data Layer
                       │
                       ▼
              Analytics Warehouse
                       │
                       ▼
                 Monitoring
```

## 2. Source Layer

The platform uses four source datasets:

- `customers.csv`
- `orders.csv`
- `products.csv`
- `customer_activity.csv`

These represent the core entities required to construct a unified customer view.

## 3. Bronze Layer

The ingestion layer loads source datasets without applying business transformations.

The raw datasets are persisted under:

```text
customer360_lake/bronze/
```

This provides a reproducible raw-data layer.

## 4. Silver Layer

The standardization layer cleans and prepares the data.

Key operations include:

- Column-name normalization
- Data-type conversion
- Customer deduplication
- Order deduplication
- Invalid-value filtering
- Date normalization
- Activity normalization

The standardized datasets are persisted under:

```text
customer360_lake/silver/
```

## 5. Customer 360 Processing

Transactions are enriched with product information.

Customer-level metrics include:

- Order count
- Total revenue
- Total units
- Average order value
- First order date
- Last order date

Activity-level metrics include:

- Login count
- Product-view count
- Support-ticket count
- Email-open count
- Purchase activity count
- Last activity date

## 6. Unified Customer Profile

The Customer 360 profile combines:

- Customer master data
- Transaction metrics
- Activity metrics
- Preferred product category
- Customer age
- Purchase frequency
- Lifetime value
- Recency
- Engagement score
- Customer status
- Profile completeness

This creates a single customer-level analytical view.

## 7. Customer Segmentation

Customers are assigned transparent business-rule segments:

- `PROSPECT`
- `VIP`
- `AT_RISK`
- `NEW_CUSTOMER`
- `LOYAL`
- `ENGAGED`
- `ACTIVE`

The rules are intentionally explainable so that analysts and business teams can understand why a customer belongs to a segment.

## 8. Gold Layer

Business-ready datasets are stored under:

```text
customer360_lake/gold/
```

The Gold layer contains:

- `customer_360_profile`
- `dim_customer`
- `fact_customer_transactions`
- `revenue_by_region`
- `revenue_by_category`
- `segment_performance`
- `top_customers`
- `segment_summary`

## 9. Analytics Warehouse

The warehouse layer provides analytics-ready views for:

- Customer lifetime value
- Regional revenue
- Segment performance
- Product-category performance
- Top customers
- At-risk customers
- Highly engaged customers
- Recent transactions

## 10. Data Quality

The platform validates:

- Required columns
- Customer ID completeness
- Customer ID uniqueness
- Non-negative revenue
- Non-negative order counts
- Non-empty profiles
- Referential integrity

A quality score of at least 95% is considered passing.

## 11. Monitoring

The monitoring layer tracks:

- Pipeline runtime
- Input record count
- Output profile count
- Quality score
- Pipeline status
- Runtime and quality alerts

The current implementation uses configurable thresholds.

## 12. Orchestration

The workflow defines the logical execution sequence:

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

Retry handling is supported for individual stages.

## 13. Technology Stack

- Python
- Pandas
- PyYAML
- Pytest
- Parquet
- SQL
- Docker

## 14. Production Extension Opportunities

A production implementation could extend this architecture with:

- Apache Airflow
- Apache Kafka
- Spark
- Cloud object storage
- Cloud data warehouses
- dbt
- Great Expectations
- Prometheus/Grafana
- CI/CD
- Metadata and data catalog systems
