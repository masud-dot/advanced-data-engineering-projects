# Project 16 — Senior-Level System Design

## 1. Business Scenario

A fintech organization needs a unified transaction analytics platform supporting near-real-time transaction processing, historical fraud analytics, executive dashboards, customer analytics, high availability, strong durability, security, and predictable operating cost.

The platform must support growth from approximately 100K events/second toward 500K events/second.

## 2. Functional Requirements

- Continuous transaction-event ingestion
- Streaming processing with a target end-to-end latency below five seconds
- 12-month historical fraud analytics
- Daily executive dashboard refresh
- Data-quality validation before trusted publication
- Operational monitoring for throughput, latency, runtime, quality, and failures

## 3. Non-Functional Requirements

| Requirement | Target |
|---|---:|
| Availability | 99.9% |
| Streaming latency | < 5 seconds |
| Historical fraud query | < 10 seconds |
| Dashboard query | < 5 minutes |
| Durability | RPO 0 |
| Recovery target | RTO 15 minutes |
| Security | SOC 2 / PCI-DSS aligned controls |
| Cost measurement | Cost per million events |

These are architectural objectives, not guarantees of the local simulation.

## 4. Capacity Planning

### Kafka

Initial peak: 100K events/second.

Projected peak: 500K events/second.

A representative starting point is 50 partitions per topic with three-way replication. Production sizing must be validated through workload testing.

### Spark

Initial workload: 500 GB/day.

Projected workload: 5 TB/day.

The production design uses autoscaling and supports a broad executor range.

### Redshift

Initial analytical storage: 10 TB.

Projected storage: 100 TB.

Warehouse sizing should account for concurrency, query patterns, storage, and workload management.

## 5. Data Modeling

### Bronze
Raw, append-oriented, replayable source representation with lineage.

### Silver
Validated, standardized, deduplicated, enriched transaction data.

### Gold
Business-ready transaction analytics, fraud events, customer summaries, executive KPIs, and merchant-category analytics.

## 6. Processing Semantics

The production system should favor idempotent processing.

Transaction ID provides a natural deduplication key.

Checkpointing allows stream processing to recover without unnecessarily reprocessing committed work.

For critical financial workloads, exactly-once behavior should be designed and validated end to end rather than assumed from a single component.

## 7. Fraud Analytics

The repository uses deterministic rules for local demonstration, including high-value transaction detection.

A production fraud platform could add feature engineering, historical behavior, risk scoring, model inference, model monitoring, human review, and feedback loops.

The local rules are not presented as a production fraud model.

## 8. Failure Scenarios

| Component | Failure | Recovery |
|---|---|---|
| Kafka broker | Broker failure | Replica/leader recovery |
| Spark | Job failure | Checkpoint-based restart |
| S3 | Data corruption | Versioned/replicated recovery |
| Redshift | Node/service failure | Managed recovery |
| Airflow | Scheduler failure | HA scheduler design |
| Processing logic | Bad deployment | Rollback and replay |
| Data quality | Invalid batch | Quality gate |

## 9. Disaster Recovery

Primary region: **us-east-1**

Secondary region: **us-west-2**

The design includes S3 cross-region replication, Kafka MirrorMaker 2, replicated Redshift snapshots, and highly available Airflow metadata services.

DR should be tested through scheduled exercises.

## 10. IAM and Security

The platform follows least privilege.

Examples:

- Kafka producers write only required topics.
- Processing jobs access required Bronze and Silver locations.
- ETL roles access only required storage prefixes.
- Warehouse loading jobs access only required Gold datasets.

Controls include encryption at rest, TLS, KMS, secret management, IAM roles, and audit logging.

## 11. Cost Optimization

Key levers include autoscaling, spot capacity where appropriate, Parquet and compression, partition pruning, incremental processing, efficient transformations, warehouse workload management, and pause/resume where supported.

Track:

**Total platform cost / millions of events processed**

## 12. Architecture Decision Records

ADR-001 selects Apache Iceberg for Silver and Gold because the platform requires ACID transactions, time travel, schema evolution, and multi-engine access.

The trade-off is additional table, catalog, and metadata-management complexity.

## 13. Local Capstone Demonstration

Run:

```bash
python -m src.production_capstone
```

The demonstration validates ingestion, processing, enrichment, quality gates, Bronze/Silver/Gold storage, warehouse loading, fraud analytics, customer analytics, and monitoring.

Docker provides the same reproducible demonstration.

## 14. Senior-Level Design Lessons

A senior data engineer evaluates architecture as a system rather than as a collection of tools.

Key questions:

1. What are the business requirements?
2. What latency and throughput are required?
3. What failures are acceptable?
4. What data must be replayable?
5. Where should validation occur?
6. How will the system scale?
7. How will security be enforced?
8. How will costs be measured?
9. How will regional failure be handled?
10. How will architecture decisions be documented?

Technology choices should follow requirements rather than the other way around.
