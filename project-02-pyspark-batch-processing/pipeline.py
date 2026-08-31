import os
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT = PROJECT_ROOT / "datasets" / "large_sales_data.csv"
DEFAULT_OUTPUT = PROJECT_ROOT / "output" / "processed_sales"


def create_spark_session() -> SparkSession:
    return (
        SparkSession.builder
        .appName("SalesBatchPipeline")
        .config("spark.sql.shuffle.partitions", "8")
        .getOrCreate()
    )


def run_pipeline(
    input_path: str | Path = DEFAULT_INPUT,
    output_path: str | Path = DEFAULT_OUTPUT,
):
    spark = create_spark_session()

    try:
        df = (
            spark.read
            .option("header", True)
            .option("inferSchema", True)
            .csv(str(input_path))
        )

        required_columns = {
            "order_id",
            "region",
            "product_name",
            "quantity",
            "price",
        }

        missing_columns = required_columns.difference(df.columns)
        if missing_columns:
            raise ValueError(
                f"Missing required columns: {sorted(missing_columns)}"
            )

        df = (
            df.withColumn(
                "total_amount",
                col("quantity") * col("price"),
            )
            .dropna()
            .dropDuplicates()
        )

        sales_summary = (
            df.groupBy("region")
            .agg(
                spark_sum("total_amount").alias("regional_sales")
            )
            .orderBy("region")
        )

        print("Regional sales summary:")
        sales_summary.show(truncate=False)

        processed_df = df.repartition(8).coalesce(4)

        processed_df.write.mode("overwrite").parquet(
            str(output_path)
        )

        jdbc_url = os.getenv("JDBC_URL")

        if jdbc_url:
            jdbc_table = os.getenv(
                "JDBC_TABLE",
                "sales_summary",
            )
            jdbc_user = os.getenv("JDBC_USER")
            jdbc_password = os.getenv("JDBC_PASSWORD")

            if not jdbc_user or not jdbc_password:
                raise RuntimeError(
                    "JDBC_USER and JDBC_PASSWORD must be set "
                    "when JDBC_URL is configured."
                )

            sales_summary.write.format("jdbc").options(
                url=jdbc_url,
                dbtable=jdbc_table,
                user=jdbc_user,
                password=jdbc_password,
                driver="org.postgresql.Driver",
            ).mode("overwrite").save()
        else:
            print(
                "JDBC_URL is not configured; "
                "skipping PostgreSQL load."
            )

        return sales_summary

    finally:
        spark.stop()


if __name__ == "__main__":
    run_pipeline()
