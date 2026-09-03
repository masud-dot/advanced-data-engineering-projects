import argparse
import json
import os
import random
import signal
import time

from kafka import KafkaProducer
from kafka.errors import KafkaError


KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:9092",
)
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "delivery_topic")

CITIES = ["Mumbai", "Delhi", "Bangalore", "Chennai"]

_running = True


def stop_producer(signum, frame):
    global _running
    _running = False
    print("\nStopping producer...")


def create_producer() -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        acks="all",
        retries=5,
    )


def create_event() -> dict:
    return {
        "order_id": random.randint(1000, 9999),
        "city": random.choice(CITIES),
        "amount": random.randint(200, 1500),
    }


def publish_events(count: int | None = None, interval: float = 1.0) -> None:
    producer = create_producer()
    published = 0

    try:
        while _running and (count is None or published < count):
            event = create_event()

            try:
                metadata = producer.send(
                    KAFKA_TOPIC,
                    value=event,
                ).get(timeout=10)

                published += 1

                print(
                    f"Published order {event['order_id']} "
                    f"city={event['city']} "
                    f"amount={event['amount']} "
                    f"partition={metadata.partition} "
                    f"offset={metadata.offset}"
                )

            except KafkaError as exc:
                print(f"Failed to publish event: {exc}")
                raise

            time.sleep(interval)

        producer.flush()
        print(f"Producer completed. Events published: {published}")

    finally:
        producer.close()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Publish synthetic delivery events to Kafka."
    )

    parser.add_argument(
        "--count",
        type=int,
        default=None,
        help="Number of events to publish. Omit for continuous mode.",
    )

    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Delay between events in seconds.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, stop_producer)
    signal.signal(signal.SIGTERM, stop_producer)

    args = parse_arguments()

    publish_events(
        count=args.count,
        interval=args.interval,
    )
