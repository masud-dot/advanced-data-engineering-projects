# Project 5 — Spark Streaming + Kafka

A production-style streaming pipeline that publishes synthetic delivery events to Apache Kafka, processes them with Spark Structured Streaming, performs 5-minute windowed city-level aggregations with watermarking, and persists the results to PostgreSQL.

## Architecture

```text
Python Producer
      |
      v
Apache Kafka
      |
      v
Spark Structured Streaming
      |
      +--> JSON parsing and validation
      |
      +--> Processing timestamps
      |
      +--> 5-minute tumbling windows
      |
      +--> 1-minute watermark
      |
      v
PostgreSQL
```

## Technology

- Python 3.10+
- Apache Kafka
- PySpark 3.5.6
- PostgreSQL 16
- Docker
- kafka-python 2.2.15

## Project Files

| File | Purpose |
|---|---|
| `producer.py` | Generates synthetic delivery events and publishes them to Kafka |
| `streaming_job.py` | Reads Kafka events, performs windowed aggregations, and writes results to PostgreSQL |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Excludes Spark Structured Streaming checkpoint data |

## Prerequisites

- Python 3.10+
- Java 17
- Apache Kafka
- PostgreSQL
- Docker Desktop

The project can use the Kafka and PostgreSQL services created for Project 4, or equivalent local services.

### Windows

When running Spark locally on Windows, Hadoop native utilities such as `winutils.exe` may be required. Use a Hadoop version compatible with the Hadoop libraries bundled with your Spark installation.

## Installation

Create a virtual environment and install the Python dependencies:

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

For Windows Command Prompt:

```cmd
.venv\Scripts\activate
```

## Kafka Configuration

Default values:

```text
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC=delivery_topic
```

Both values can be overridden with environment variables.

The producer generates synthetic delivery events with this structure:

```json
{
  "order_id": 1001,
  "city": "Mumbai",
  "amount": 750
}
```

Available cities:

- Mumbai
- Delhi
- Bangalore
- Chennai

## PostgreSQL Configuration

Default connection settings:

```text
DATABASE_URL=jdbc:postgresql://localhost:5432/data_engineering
DATABASE_USER=postgres
DATABASE_PASSWORD=admin
```

These values can be overridden with environment variables.

The streaming job writes aggregated results to:

```text
city_sales_stream
```

Output columns:

| Column | Description |
|---|---|
| `window_start` | Start of the aggregation window |
| `window_end` | End of the aggregation window |
| `city` | Delivery city |
| `window_sales` | Total sales amount for the city and window |

> For public or production deployments, use environment variables or a secret-management solution instead of real credentials.

## Run the Producer

### Publish a fixed number of events

```bash
python producer.py --count 10
```

### Run continuously

```bash
python producer.py
```

Stop it with `Ctrl+C`.

### Control event rate

```bash
python producer.py --count 20 --interval 0.5
```

The producer reports the Kafka partition and offset for each successfully published event.

## Run Spark Structured Streaming

Start the Spark streaming application:

```bash
python streaming_job.py
```

The application:

1. Connects to Kafka.
2. Reads events from `delivery_topic`.
3. Converts Kafka values from JSON text into structured columns.
4. Validates `order_id`, `city`, and `amount`.
5. Adds a processing timestamp.
6. Applies a 5-minute tumbling window.
7. Applies a 1-minute watermark.
8. Aggregates sales by city.
9. Writes each micro-batch to PostgreSQL.

The Spark application uses a checkpoint directory:

```text
./spark_checkpoint
```

This directory is intentionally excluded from Git.

Stop the application with:

```text
Ctrl+C
```

## Verify PostgreSQL Results

If PostgreSQL is running in the Project 4 Docker container:

```bash
docker exec -it project-04-kafka-realtime-streaming-postgres-1 psql -U postgres -d data_engineering -c "SELECT * FROM city_sales_stream ORDER BY window_start DESC, city LIMIT 20;"
```

Example result:

```text
    window_start     |     window_end      |   city    | window_sales
---------------------+---------------------+-----------+--------------
 2026-09-03 11:35:00 | 2026-09-03 11:40:00 | Bangalore |        27930
 2026-09-03 11:35:00 | 2026-09-03 11:40:00 | Chennai   |        24290
 2026-09-03 11:35:00 | 2026-09-03 11:40:00 | Delhi     |        24276
 2026-09-03 11:35:00 | 2026-09-03 11:40:00 | Mumbai    |        21678
```

Exact values vary because the producer generates random synthetic events.

## Environment Variables

| Variable | Default | Purpose |
|---|---|---|
| `KAFKA_BOOTSTRAP_SERVERS` | `localhost:9092` | Kafka broker address |
| `KAFKA_TOPIC` | `delivery_topic` | Kafka topic |
| `DATABASE_URL` | `jdbc:postgresql://localhost:5432/data_engineering` | PostgreSQL JDBC URL |
| `DATABASE_USER` | `postgres` | PostgreSQL username |
| `DATABASE_PASSWORD` | `admin` | PostgreSQL password |
| `CHECKPOINT_DIR` | `./spark_checkpoint` | Spark checkpoint directory |
| `WINDOW_DURATION` | `5 minutes` | Aggregation window duration |
| `WATERMARK_DELAY` | `1 minute` | Watermark delay |

## Design Notes

### Windowed Aggregation

Events are grouped by city and a 5-minute tumbling processing-time window. This converts individual streaming events into time-based sales summaries.

### Watermarking

A 1-minute watermark allows Spark to manage late data while limiting the amount of state retained for the streaming aggregation.

### Checkpointing

Spark Structured Streaming uses the checkpoint directory to maintain streaming progress and state. The checkpoint directory is runtime data and should not be committed to source control.

### Reliability

The Kafka producer uses:

- `acks="all"`
- Multiple retries
- Explicit delivery confirmation
- Graceful shutdown handling

The producer supports both finite test runs and continuous streaming.

## Troubleshooting

### Kafka connection refused

Make sure Kafka is running and listening on:

```text
localhost:9092
```

Check Docker containers:

```bash
docker ps
```

### PostgreSQL connection problems

Verify that PostgreSQL is running and that the `data_engineering` database exists.

### Spark cannot start on Windows

Check that Java 17 is installed and that the required Hadoop native utilities are configured correctly.

### PostgreSQL timezone error

The Spark application configures UTC-related timezone settings because PostgreSQL JDBC connections can otherwise inherit an incompatible local JVM timezone.

## Safety

Never commit:

- Real passwords
- API keys
- Cloud credentials
- Production data
- Personal information

Use synthetic data and environment variables for public repositories.

## Book

This repository is the companion implementation for:

**Advanced Data Engineering Projects with Python, SQL & Cloud**

The project demonstrates Kafka-based event streaming, Spark Structured Streaming, windowed aggregations, watermarking, checkpointing, and PostgreSQL persistence.
