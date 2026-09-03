import json
import os
import time

from kafka import KafkaProducer
from kafka.errors import KafkaError


KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:9092",
)
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "orders_topic")


ORDERS = [
    {
        "order_id": 1001,
        "customer": "Alice",
        "product": "Laptop",
        "quantity": 1,
        "amount": 75000,
    },
    {
        "order_id": 1002,
        "customer": "Bob",
        "product": "Keyboard",
        "quantity": 2,
        "amount": 4000,
    },
]


def create_producer() -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        acks="all",
        retries=5,
    )


def publish_orders() -> None:
    producer = create_producer()

    try:
        for order in ORDERS:
            future = producer.send(KAFKA_TOPIC, value=order)

            try:
                metadata = future.get(timeout=10)
                print(
                    f"Published order {order['order_id']} "
                    f"to {metadata.topic} partition={metadata.partition} "
                    f"offset={metadata.offset}"
                )
            except KafkaError as exc:
                print(
                    f"Failed to publish order "
                    f"{order['order_id']}: {exc}"
                )
                raise

            time.sleep(1)

        producer.flush()
        print("All orders published successfully.")

    finally:
        producer.close()


if __name__ == "__main__":
    publish_orders()
