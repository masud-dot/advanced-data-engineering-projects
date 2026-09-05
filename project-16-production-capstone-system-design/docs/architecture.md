# Project 16 — Production Architecture

## 1. Purpose

This project is a senior-level production system-design capstone for a fintech transaction analytics platform.

The design demonstrates how a modern data platform can ingest high-volume transaction events, process them in batch and streaming paths, maintain governed Bronze/Silver/Gold data layers, serve analytical workloads, and operate with reliability, security, monitoring, and disaster recovery.

The repository also contains a runnable local implementation. The local implementation intentionally simulates cloud and distributed services so the project can run without AWS accounts, Kafka brokers, Spark clusters, or production credentials.

## 2. Production Reference Architecture

```text
Source Systems
      |
      v
Kafka --> Spark Structured Streaming --> S3 + Iceberg
                                      Bronze -> Silver -> Gold
                                                |
                                                v
                                           Redshift
                                                |
                                                v
                                      BI / Fraud Analytics

Cross-cutting: Airflow | Data Quality | Prometheus | IAM | Security | DR | Cost
```

## 3. Major Components

### Kafka
Production event-ingestion layer providing durable event storage, partitioned parallelism, consumer groups, replay, and high-throughput ingestion.

### Spark Structured Streaming
Production processing engine for parsing, validation, deduplication, cleansing, enrichment, incremental processing, and checkpoint-based recovery.

### S3 and Apache Iceberg
S3 provides durable object storage while Iceberg provides a table abstraction supporting ACID operations, schema evolution, time travel, and multi-engine access.

### Redshift
Production analytical warehouse for curated Gold data and executive analytics.

### Airflow
Coordinates batch workflows, dependencies, retries, scheduling, and operational workflows.

### Prometheus
Represents the production monitoring layer for pipeline metrics, latency, throughput, failures, and service health.

## 4. Local Implementation Mapping

| Production | Local implementation |
|---|---|
| Kafka | `SimulatedKafkaStream` |
| Spark Structured Streaming | `SimulatedSparkProcessor` using Pandas |
| S3 | `production_lake/` |
| Iceberg | `LocalIcebergTable` Parquet abstraction |
| Redshift | `LocalRedshiftWarehouse` |
| Airflow | `SimulatedAirflowWorkflow` |
| Prometheus | `LocalPrometheusExporter` |
| Production data | Synthetic CSV files |

The local implementation is an educational simulation of the production contracts. It does not claim to execute Kafka, Spark, S3, Iceberg, Redshift, Airflow, or Prometheus locally.

## 5. Data Flow

1. Transaction events enter ingestion.
2. Events are captured by the simulated Kafka stream.
3. Processing validates timestamps, amounts, identifiers, and status.
4. Duplicate transaction IDs are removed.
5. Customer information is joined to transactions.
6. Raw events are retained in Bronze.
7. Validated/enriched transactions are written to Silver.
8. Fraud rules and customer analytics produce Gold datasets.
9. Analytical tables are loaded into the warehouse abstraction.
10. Quality and monitoring metrics are emitted.
11. Executive metrics are generated.

## 6. Reliability Principles

The platform uses idempotent processing, checkpoint-based recovery, durable event retention, data validation, retryable orchestration, health and quality gates, multi-region disaster recovery, least-privilege access, and encryption.

Target availability is 99.9%.

## 7. Security Boundary

Production deployments should use IAM roles, KMS-managed encryption, TLS, secret-manager based credentials, least-privilege policies, audit logging, and network controls.

Sensitive credentials and production data must never be committed to this repository.

## 8. Scaling Strategy

Kafka scales through partitions and brokers. Spark scales through executors and workload parallelism. S3 scales storage independently from compute. Redshift scales analytical workloads according to storage, concurrency, and query requirements. Airflow workers scale with workflow concurrency.

## 9. Architectural Trade-offs

The design accepts additional operational complexity in exchange for high throughput, replayability, fault isolation, independent scaling, analytical flexibility, schema evolution, and operational visibility.

For smaller workloads, a simpler managed ETL and warehouse architecture may be more appropriate.

The correct architecture depends on workload, reliability requirements, data volume, latency, team capability, and budget.
