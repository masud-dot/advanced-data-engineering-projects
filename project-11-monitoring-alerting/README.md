# Project 11 — Monitoring & Alerting System

A practical monitoring and alerting framework for data engineering pipelines. This project captures pipeline execution metrics, performs health checks, evaluates threshold-based alert rules, stores monitoring history, and provides console, email, and Slack notification patterns.

## Project Overview

Production data pipelines can fail silently, become slower over time, process fewer records than expected, or produce poor-quality data. A monitoring layer helps engineering teams detect these problems early.

This project demonstrates a reusable monitoring architecture built around:

- Pipeline execution metrics
- Runtime and duration tracking
- Success/failure tracking
- Input and output row monitoring
- Error-rate monitoring
- Data-quality scoring
- Freshness monitoring
- Threshold-based health checks
- Warning and critical alerts
- Structured JSON logging
- Alert history persistence
- Console notification
- Email notification payloads
- Slack notification payloads
- SQL monitoring and reporting patterns
- Docker-based execution

## Architecture

```text
                         DATA PIPELINE
                              |
              +---------------+---------------+
              |               |               |
              v               v               v
           Metrics           Logs        Data Quality
              |               |               |
              +---------------+---------------+
                              |
                              v
                    MONITORING ENGINE
                              |
                    +---------+---------+
                    |                   |
                    v                   v
                Health Checks       Alert Rules
                    |                   |
                    +---------+---------+
                              |
                              v
                       ALERT DISPATCHER
                              |
                  +-----------+-----------+
                  |           |           |
                  v           v           v
               Console      Email       Slack
```

## Monitoring Capabilities

### 1. Execution Metrics

Each pipeline run records:

- Run ID
- Pipeline name
- Status
- Start timestamp
- End timestamp
- Duration
- Input row count
- Output row count
- Error count
- Quality score

Metrics are persisted in JSON format for local monitoring history.

### 2. Health Checks

The monitoring engine evaluates:

| Health Check | Purpose |
|---|---|
| Output Volume | Detects unexpectedly low output |
| Error Rate | Detects excessive processing errors |
| Duration | Detects slow pipeline execution |
| Quality Score | Detects poor data quality |
| Freshness | Provides a freshness validation pattern |

A check is reported as `HEALTHY` or `UNHEALTHY`.

### 3. Alert Rules

The alert engine evaluates configured thresholds.

| Rule | Severity | Condition |
|---|---|---|
| Duration threshold | WARNING | Runtime exceeds configured maximum |
| Error threshold | CRITICAL | Error count exceeds allowed maximum |
| Volume threshold | CRITICAL | Output rows fall below minimum |
| Quality threshold | CRITICAL | Quality score falls below minimum |

Example configuration:

```yaml
thresholds:
  max_error_rate: 0.10
  max_duration_seconds: 30
  max_error_count: 0
  min_quality_score: 0.95
  min_output_rows: 1
```

## Project Structure

```text
project-11-monitoring-alerting/
├── README.md
├── requirements.txt
├── Dockerfile
├── .gitignore
│
├── monitoring/
│   ├── metrics.py
│   ├── health.py
│   ├── alerts.py
│   ├── logger.py
│   └── monitor.py
│
├── pipelines/
│   └── monitored_pipeline.py
│
├── alerts/
│   ├── console.py
│   ├── email.py
│   └── slack.py
│
├── configs/
│   └── monitoring.yaml
│
├── sample_data/
│   └── sales_data.csv
│
├── sql/
│   └── monitoring_queries.sql
│
├── src/
│   └── monitoring_pipeline.py
│
└── tests/
    ├── test_metrics.py
    ├── test_alerts.py
    ├── test_health.py
    └── test_pipeline.py
```

## Key Components

### `monitoring/metrics.py`

Defines the `PipelineMetrics` model and provides functionality for:

- Calculating execution duration
- Calculating quality score
- Converting metrics to dictionaries
- Persisting metrics
- Loading historical metrics

### `monitoring/health.py`

Contains reusable health-check functions for:

- Output volume
- Error rate
- Duration
- Quality score
- Freshness

### `monitoring/alerts.py`

Implements threshold-based alert evaluation and alert persistence.

Alerts include:

- Alert ID
- Pipeline name
- Severity
- Rule
- Message
- Creation timestamp

### `monitoring/logger.py`

Provides structured JSON logging with configurable log level and optional file output.

Example:

```json
{
  "timestamp": "2026-09-05 11:52:59,730",
  "level": "INFO",
  "message": "Pipeline started: sales_monitoring_pipeline"
}
```

### `monitoring/monitor.py`

The `MonitoringEngine` coordinates:

1. Metrics creation
2. Health checks
3. Alert evaluation
4. Metrics persistence
5. Alert persistence
6. Monitoring completion logging

### `pipelines/monitored_pipeline.py`

Runs the sample sales pipeline and connects pipeline processing with the monitoring engine.

The sample pipeline:

1. Loads sales data
2. Validates records
3. Identifies invalid transactions
4. Produces cleaned output
5. Calculates quality metrics
6. Records execution metrics
7. Runs health checks
8. Generates alerts when thresholds are breached
9. Dispatches alerts to the console

### `alerts/`

Contains notification patterns for:

- Console
- Email
- Slack

The email and Slack modules currently build/send notification payloads as integration patterns. External SMTP or Slack HTTP delivery is not live-configured in this local project.

## Configuration

The monitoring configuration is stored in:

```text
configs/monitoring.yaml
```

Example:

```yaml
pipeline:
  name: sales_monitoring_pipeline
  freshness_threshold_minutes: 60
  max_error_rate: 0.10
  min_output_rows: 1

alerts:
  enabled: true
  severity_levels:
    - INFO
    - WARNING
    - CRITICAL

thresholds:
  max_error_rate: 0.10
  max_duration_seconds: 30
  max_error_count: 0
  min_quality_score: 0.95
  min_output_rows: 1

logging:
  level: INFO
  log_file: local_output/pipeline.log

storage:
  metrics_file: local_output/metrics.json
  alerts_file: local_output/alerts.json
```

## Running Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the automated tests

```bash
python -m pytest -q
```

Expected result for the validated project:

```text
14 passed
```

### 3. Run the monitoring pipeline

From the project root:

```bash
python -m src.monitoring_pipeline
```

Running the file directly with:

```bash
python src/monitoring_pipeline.py
```

may fail because the project root is not automatically placed on the Python module search path. The module form is therefore the recommended command.

### Example Successful Run

The validated sample pipeline produced:

```text
Status         : SUCCESS
Input rows     : 10
Output rows    : 10
Errors         : 0
Quality score  : 100.00%
Duration       : 0.010s

Health Checks:
- output_volume: HEALTHY
- error_rate: HEALTHY
- duration: HEALTHY
- quality_score: HEALTHY

Alerts generated: 0
```

## Generated Monitoring Artifacts

Successful local execution creates:

```text
local_output/
├── metrics.json
├── processed_sales.csv
└── pipeline.log
```

An `alerts.json` file is created when alerts are persisted.

The local output directory is excluded from Git through `.gitignore`.

## Alert Validation

The alert engine was also tested with deliberately unhealthy metrics.

Example test conditions:

- Duration: 45 seconds
- Error count: 2
- Output rows: 0
- Quality score: 80%

The engine correctly generated four alerts:

```text
WARNING  | duration_threshold
CRITICAL | error_threshold
CRITICAL | volume_threshold
CRITICAL | quality_threshold
```

This confirms that the monitoring layer detects both healthy and unhealthy execution conditions.

## SQL Monitoring

`sql/monitoring_queries.sql` contains reusable query patterns for monitoring systems, including:

- Recent executions
- Failed executions
- Slow executions
- Volume anomalies
- Low-quality runs
- Alert history
- Critical alerts
- Daily success rate
- Average runtime

These SQL examples are intended to be adapted to a production monitoring database or warehouse.

## Docker

Build the image:

```bash
docker build -t monitoring-alerting .
```

Run:

```bash
docker run --rm monitoring-alerting
```

The Docker image uses Python 3.11-slim and starts the monitoring entry point with:

```text
python src/monitoring_pipeline.py
```

For container execution, the image is built with the project root as the working directory.

## Production Architecture

A production implementation can extend this local framework with services such as:

```text
                    Data Pipeline
                         |
                         v
              Monitoring / Metrics Layer
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
      Prometheus      CloudWatch      OpenTelemetry
          |              |              |
          +--------------+--------------+
                         |
                         v
                    Alert Rules
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
       Grafana        Slack           Email
```

Typical production integrations could include:

- Apache Airflow
- AWS CloudWatch
- Prometheus
- Grafana
- OpenTelemetry
- Slack
- SMTP/email services
- Cloud data warehouses
- Centralized logging platforms

The current repository demonstrates the monitoring architecture locally rather than claiming live integration with these external services.

## Testing

The project includes unit and integration-style tests covering:

- Duration calculation
- Quality-score calculation
- Metric serialization
- Output-volume checks
- Error-rate checks
- Duration checks
- Quality checks
- Alert generation
- End-to-end pipeline execution
- Monitoring artifact creation

Validated result:

```text
14 passed in 0.98s
```

## Validation Status

The following validations have been completed:

- [x] Python modules compile successfully
- [x] Automated test suite passes
- [x] Sample pipeline executes successfully
- [x] Metrics are persisted
- [x] Processed output is generated
- [x] Healthy health checks verified
- [x] Alert generation verified
- [x] Structured logging verified
- [x] Docker configuration included
- [x] SQL monitoring patterns included

External cloud services such as AWS, live Slack delivery, and live SMTP email delivery were not executed as part of local validation.

## Learning Outcomes

After completing this project, you should understand how to:

- Design a monitoring layer for data pipelines
- Capture pipeline execution metrics
- Measure runtime and data volume
- Calculate and monitor data quality
- Detect excessive error rates
- Build threshold-based alert rules
- Separate health checks from alert evaluation
- Persist monitoring history
- Implement structured logging
- Design notification integrations
- Create SQL monitoring reports
- Containerize a monitoring application
- Extend a local monitoring framework toward production observability platforms

## Conclusion

This project demonstrates a practical foundation for monitoring modern data engineering pipelines. Instead of treating monitoring as an afterthought, the framework places metrics, health checks, alerts, and structured logging directly around pipeline execution.

The implementation is intentionally lightweight enough to run locally while providing a clear path toward production integrations with orchestration, cloud monitoring, observability, and notification platforms.
