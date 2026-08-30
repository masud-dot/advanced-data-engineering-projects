# Technology Selection

| Area | Selected | Rationale |
|---|---|---|
| Event ingestion | Apache Kafka | High throughput, retention, replay |
| Stream processing | Spark Structured Streaming | Unified batch/stream API |
| Storage | S3 + Apache Iceberg | Open format, ACID, time travel |
| Warehouse | Amazon Redshift | AWS-native analytics |
| Orchestration | Apache Airflow | Mature workflow ecosystem |
