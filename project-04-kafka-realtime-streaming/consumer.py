import json
import os

import pandas as pd
from kafka import KafkaConsumer
from sqlalchemy import create_engine


KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:9092",
)
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "orders_topic")
KAFKA_GROUP_ID = os.getenv(
    "KAFKA_GROUP_ID",
    "order_processing_group",
)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:admin@localhost:5432/data_engineering",
)


def create_consumer() -> KafkaConsumer:
    return KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id=KAFKA_GROUP_ID,
        value_deserializer=lambda value: json.loads(
            value.decode("utf-8")
        ),
    )


def persist_order(order: dict, engine) -> None:
    dataframe = pd.DataFrame([order])

    dataframe.to_sql(
        "live_orders",
        engine,
        if_exists="append",
        index=False,
    )

    print(f"Persisted order {order['order_id']}")


def consume_orders() -> None:
    engine = create_engine(DATABASE_URL)
    consumer = create_consumer()

    print(
        f"Listening on topic '{KAFKA_TOPIC}' "
        f"using group '{KAFKA_GROUP_ID}'..."
    )

    try:
        for message in consumer:
            order = message.value
            persist_order(order, engine)
    finally:
        consumer.close()
        engine.dispose()


if __name__ == "__main__":
    consume_orders()
