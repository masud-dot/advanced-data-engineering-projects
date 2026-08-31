from pyspark.sql import SparkSession

from optimisations import (
    optimise_with_broadcast,
    repartition_for_processing,
)


def test_broadcast_join():
    spark = (
        SparkSession.builder
        .master("local[2]")
        .appName("test-broadcast-join")
        .getOrCreate()
    )

    try:
        large_df = spark.createDataFrame(
            [
                (1, "East", 75000),
                (2, "West", 4000),
            ],
            ["order_id", "region", "total_amount"],
        )

        lookup_df = spark.createDataFrame(
            [
                ("East", "Eastern Region"),
                ("West", "Western Region"),
            ],
            ["region", "region_name"],
        )

        result = optimise_with_broadcast(
            large_df,
            lookup_df,
            "region",
        )

        assert result.count() == 2
        assert "region_name" in result.columns

    finally:
        spark.stop()


def test_repartition():
    spark = (
        SparkSession.builder
        .master("local[2]")
        .appName("test-repartition")
        .getOrCreate()
    )

    try:
        df = spark.createDataFrame(
            [(1,), (2,), (3,)],
            ["id"],
        )

        result = repartition_for_processing(df, 2)

        assert result.rdd.getNumPartitions() == 2

    finally:
        spark.stop()
