# Project 16 — Operations Runbook

## 1. Purpose

This document describes how an engineering team can operate, validate, troubleshoot, and recover the production-style data platform.

The repository provides a local simulation for these operational concepts.

## 2. Normal Local Execution

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run tests:

```bash
python -m pytest -q
```

Run the capstone:

```bash
python -m src.production_capstone
```

Compile-check Python files:

```bash
python -m compileall -q .
```

Generated artifacts include:

- `production_lake/`
- `local_warehouse/`
- `monitoring_output/`

These directories are intentionally ignored by Git.

## 3. Expected Successful Run

A healthy run should report successful ingestion, processing, a quality score at or above the configured threshold, pipeline status `SUCCESS`, successful stages, and generated monitoring metrics.

The sample implementation processes 30 synthetic transactions and currently produces a 100% quality score.

Runtime is environment-dependent and is not a production SLA.

## 4. Monitoring

The monitoring layer records:

- Input record count
- Output record count
- Quality score
- Error count
- Runtime
- Stage status

The local exporter writes:

```text
monitoring_output/pipeline_metrics.json
```

A production implementation should expose metrics to Prometheus and provide operational dashboards.

Recommended alerts include:

- Streaming latency above five seconds
- Pipeline runtime above threshold
- Quality score below threshold
- Consumer lag growth
- Processing error spikes
- Warehouse load failures
- Storage failures
- Missing expected data

## 5. Data Quality Operations

Quality checks run before trusted analytical publication.

Current checks include required columns, unique transaction IDs, valid customer identifiers, non-negative amounts, and valid timestamps.

A failed quality gate should prevent bad data from becoming trusted Gold data.

Production financial systems should also consider referential integrity, currency validation, amount precision, business rules, freshness, volume anomalies, and source reconciliation.

## 6. Incident Response

### Detect
Use monitoring alerts and dashboards.

### Classify
Determine whether the issue is ingestion, processing, storage, quality, warehouse, orchestration, infrastructure, or security.

### Contain
Prevent bad data or repeated failures from propagating.

### Recover
Use Kafka replay, checkpoint restart, data restore, warehouse recovery, workflow retry, or rollback as appropriate.

### Validate
Run quality checks, compare counts, check duplicates, validate downstream tables, and confirm monitoring health.

### Close
Document root cause, impact, timeline, recovery actions, and preventive actions.

## 7. Common Failure Playbooks

### Kafka broker failure

1. Confirm broker health.
2. Check partition leadership and replication.
3. Verify consumer lag.
4. Allow replica/leader recovery.
5. Confirm processing latency returns to normal.

Representative target: less than 30 seconds.

### Spark processing failure

1. Identify failed application or stage.
2. Inspect logs and metrics.
3. Validate checkpoint availability.
4. Restart from the last valid checkpoint.
5. Confirm no duplicate publication.
6. Reconcile output counts.

### Storage corruption

1. Stop affected publication.
2. Identify impacted objects/tables.
3. Restore a known-good or replicated copy.
4. Reconcile data.
5. Resume downstream processing.

### Warehouse failure

1. Confirm warehouse health.
2. Check loading status.
3. Retry safe failed loads.
4. Validate Gold-to-warehouse reconciliation.
5. Confirm dashboard recovery.

### Airflow scheduler failure

1. Confirm scheduler availability.
2. Validate the metadata database.
3. Fail over to the standby scheduler where configured.
4. Check queued and running tasks.
5. Resume missed workflows safely.

## 8. Deployment Checklist

Before deployment:

- Run automated tests.
- Run compile checks.
- Run quality validation.
- Review schema changes.
- Review IAM changes.
- Review infrastructure changes.
- Validate rollback strategy.
- Confirm monitoring and alerts.
- Confirm secrets are externalized.

After deployment:

- Validate pipeline execution.
- Check latency.
- Check record counts.
- Check quality score.
- Check warehouse loads.
- Check alerts.
- Observe the system during the deployment window.

## 9. Disaster Recovery Exercise

Periodically simulate:

1. Primary-region loss.
2. Failover to the secondary region.
3. Storage recovery.
4. Event-processing recovery.
5. Analytical workload recovery.
6. Data reconciliation.
7. Return to normal operations.

Measure actual RTO and RPO against documented targets.

## 10. Security Operations

Regularly review:

- IAM policies
- Role usage
- Secret rotation
- KMS access
- Audit logs
- Network access
- Data-access patterns

Least privilege should be continuously reviewed.

## 11. Cost Operations

Track:

- Events processed
- Storage consumed
- Compute hours
- Warehouse usage
- Streaming infrastructure cost
- Monitoring cost

A useful business metric is:

**Total platform cost / millions of events processed**

Unexpected changes should trigger investigation.

## 12. Local vs Production Boundary

The local project is designed for learning, testing, and demonstration.

It does not provide a real Kafka cluster, Spark cluster, S3 service, Iceberg catalog, Redshift cluster, Airflow deployment, Prometheus server, or production-grade HA.

Those services are represented through explicit local abstractions.

This boundary is intentional: the repository demonstrates production architecture and operational reasoning without requiring cloud infrastructure or exposing credentials.

## 13. Operational Principle

A production data platform is not complete when the pipeline works once.

It is complete when the team can:

- Observe it
- Secure it
- Scale it
- Test it
- Recover it
- Explain it
- Control its cost
- Prove its data quality

That is the central operational lesson of this capstone.
