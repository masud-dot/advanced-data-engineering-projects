from pyspark.sql import DataFrame
from pyspark.sql.functions import col, current_timestamp, sum as spark_sum


def clean_and_transform(df: DataFrame) -> DataFrame:
    """Clean source records and calculate transaction totals."""
    required_columns = {
        "order_id",
        "customer_id",
        "region",
        "product",
        "quantity",
        "price",
    }

    missing_columns = required_columns.difference(df.columns)

    if missing_columns:
        raise ValueError(
            f"Source data is missing required columns: "
            f"{sorted(missing_columns)}"
        )

    return (
        df.select(
            "order_id",
            "customer_id",
            "region",
            "product",
            "quantity",
            "price",
            *(
                ["order_date"]
                if "order_date" in df.columns
                else []
            ),
        )
        .dropDuplicates()
        .dropna(
            subset=[
                "order_id",
                "customer_id",
                "region",
                "product",
                "quantity",
                "price",
            ]
        )
        .filter(col("quantity") > 0)
        .filter(col("price") >= 0)
        .withColumn(
            "total_amount",
            col("quantity") * col("price"),
        )
        .withColumn(
            "processed_time",
            current_timestamp(),
        )
    )


def build_regional_summary(df: DataFrame) -> DataFrame:
    """Aggregate sales by region."""
    return (
        df.groupBy("region")
        .agg(
            spark_sum("total_amount").alias("regional_sales")
        )
        .orderBy("region")
    )
