# Project 4 — Real-Time Streaming Pipeline with Kafka

A practical real-time data engineering pipeline that publishes order events to Apache Kafka, consumes them with Python, and persists the events into PostgreSQL.

## Architecture

```text
Python Producer
      |
      v
 Kafka Topic: orders_topic
      |
      v
Python Consumer
      |
      v
 PostgreSQL
      |
      v
   live_orders

## Technology

- Python
- Apache Kafka
- ZooKeeper
- PostgreSQL
- kafka-python
- Pandas
- SQLAlchemy
- Docker Compose

## Project Structure

project-04-kafka-realtime-streaming/
├── consumer.py
├── producer.py
├── docker-compose.yml
├── requirements.txt
└── README.md

## How It Works

The producer creates synthetic order events and publishes them to the orders_topic Kafka topic.

The consumer subscribes to the topic, receives the events, and persists them into the PostgreSQL live_orders table.

Kafka and PostgreSQL run locally using Docker Compose.

## Prerequisites

- Python 3.10+
- Docker Desktop
- Docker Compose

## 1. Install Python Dependencies

python -m pip install -r requirements.txt

## 2. Start Kafka and PostgreSQL

docker compose up -d

Verify the services:

docker compose ps

Kafka, ZooKeeper, and PostgreSQL should be running. PostgreSQL should report a healthy status.

## 3. Start the Consumer

Open a terminal and run:

python consumer.py

The consumer continuously listens for events.

## 4. Publish Orders

Open another terminal in the project directory and run:

python producer.py

Example output:

Published order 1001 to orders_topic partition=0 offset=0
Published order 1002 to orders_topic partition=0 offset=1
All orders published successfully.

## 5. Verify PostgreSQL

After the consumer processes the messages:

docker compose exec postgres psql -U postgres -d data_engineering -c "SELECT * FROM live_orders ORDER BY order_id;"

Expected result:

1001 | Alice | Laptop   | 1 | 75000
1002 | Bob   | Keyboard | 2 | 4000

## Configuration

The following environment variables can override the defaults.

Kafka:

KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC=orders_topic
KAFKA_GROUP_ID=order_processing_group

PostgreSQL:

DATABASE_URL=postgresql://postgres:admin@localhost:5432/data_engineering

For production environments, credentials should be supplied through secure secrets management rather than committed to source control.

## Stop the Environment

docker compose down

## Learning Objectives

This project demonstrates:

- Kafka producers and consumers
- Kafka topics and consumer groups
- Event-driven data ingestion
- JSON message serialization
- Producer acknowledgements and retries
- PostgreSQL persistence
- SQLAlchemy database connectivity
- Environment-based configuration
- Dockerized infrastructure
- Real-time streaming pipeline design

## Source

This repository is the companion implementation for *Advanced Data Engineering Projects with Python, SQL & Cloud*. Code follows the manuscript's project examples and is designed for public GitHub use.

## Safety

Never commit real credentials, API keys, cloud account IDs, or production data. Use environment variables and synthetic data.
