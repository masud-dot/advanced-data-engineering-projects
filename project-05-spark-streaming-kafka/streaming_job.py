import os
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    current_timestamp,
    from_json,
    sum as spark_sum,
    window,
)
from pyspark.sql.types import (
    IntegerType,
    StringType,
    StructField,
    StructType,
)


KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:9092",
)

KAFKA_TOPIC = os.getenv(
    "KAFKA_TOPIC",
    "delivery_topic",
)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "jdbc:postgresql://localhost:5432/data_engineering",
)

DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "admin")

CHECKPOINT_DIR = os.getenv(
    "CHECKPOINT_DIR",
    str(Path.cwd() / "spark_checkpoint"),
)

WINDOW_DURATION = os.getenv("WINDOW_DURATION", "5 minutes")
WATERMARK_DELAY = os.getenv("WATERMARK_DELAY", "1 minute")


def create_spark_session() -> SparkSession:
    return (
        SparkSession.builder
        .appName("KafkaSparkStreaming")
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.driver.extraJavaOptions", "-Duser.timezone=UTC")
        .config("spark.executor.extraJavaOptions", "-Duser.timezone=UTC")
        .config(
            "spark.jars.packages",
            ",".join(
                [
                    "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.6",
                    "org.postgresql:postgresql:42.7.8",
                ]
            ),
        )
        .getOrCreate()
    )


def create_event_schema() -> StructType:
    return StructType(
        [
            StructField("order_id", IntegerType(), True),
            StructField("city", StringType(), True),
            StructField("amount", IntegerType(), True),
        ]
    )


def write_to_postgres(
    batch_df,
    batch_id: int,
) -> None:
    if batch_df.isEmpty():
        return

    output_df = batch_df.select(
        col("window.start").alias("window_start"),
        col("window.end").alias("window_end"),
        col("city"),
        col("window_sales"),
    )

    print(f"Writing batch {batch_id} to PostgreSQL...")

    (
        output_df.write
        .format("jdbc")
        .option("url", DATABASE_URL)
        .option("dbtable", "city_sales_stream")
        .option("user", DATABASE_USER)
        .option("password", DATABASE_PASSWORD)
        .option("driver", "org.postgresql.Driver")
        .mode("append")
        .save()
    )

    print(f"Batch {batch_id} written successfully.")


def build_stream(spark: SparkSession):
    raw_stream = (
        spark.readStream
        .format("kafka")
        .option(
            "kafka.bootstrap.servers",
            KAFKA_BOOTSTRAP_SERVERS,
        )
        .option("subscribe", KAFKA_TOPIC)
        .option("startingOffsets", "earliest")
        .option("failOnDataLoss", "false")
        .load()
    )

    schema = create_event_schema()

    parsed_stream = (
        raw_stream
        .selectExpr("CAST(value AS STRING) AS json_str")
        .select(
            from_json(
                col("json_str"),
                schema,
            ).alias("data")
        )
        .select("data.*")
        .filter(
            col("order_id").isNotNull()
            & col("city").isNotNull()
            & col("amount").isNotNull()
        )
        .withColumn(
            "processing_time",
            current_timestamp(),
        )
    )

    return (
        parsed_stream
        .withWatermark(
            "processing_time",
            WATERMARK_DELAY,
        )
        .groupBy(
            window(
                col("processing_time"),
                WINDOW_DURATION,
            ),
            col("city"),
        )
        .agg(
            spark_sum("amount").alias("window_sales")
        )
    )


def main() -> None:
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")

    checkpoint_path = Path(CHECKPOINT_DIR).resolve()
    checkpoint_path.mkdir(parents=True, exist_ok=True)

    print("Starting Spark Structured Streaming...")
    print(f"Kafka: {KAFKA_BOOTSTRAP_SERVERS}")
    print(f"Topic: {KAFKA_TOPIC}")
    print(f"Checkpoint: {checkpoint_path}")

    windowed_sales = build_stream(spark)

    query = (
        windowed_sales.writeStream
        .foreachBatch(write_to_postgres)
        .outputMode("update")
        .option(
            "checkpointLocation",
            str(checkpoint_path),
        )
        .trigger(processingTime="5 seconds")
        .start()
    )

    print("Streaming query started. Press Ctrl+C to stop.")

    try:
        query.awaitTermination()
    except KeyboardInterrupt:
        print("\nStopping Spark streaming query...")
        query.stop()
    finally:
        spark.stop()
        print("Spark streaming application stopped.")


if __name__ == "__main__":
    main()
