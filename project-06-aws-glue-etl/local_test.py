from pathlib import Path

from pyspark.sql import SparkSession

from transformations import build_regional_summary, clean_and_transform


BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "sample_data" / "sales_data.csv"
OUTPUT_DIR = BASE_DIR / "local_output"


def main():
    spark = (
        SparkSession.builder
        .appName("AWSGlueETLLocalTest")
        .master("local[*]")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    try:
        print("Reading sample sales data...")

        source_df = (
            spark.read
            .option("header", True)
            .option("inferSchema", True)
            .csv(str(INPUT_FILE))
        )

        print(f"Source records: {source_df.count()}")

        transformed_df = clean_and_transform(source_df)

        print(f"Cleaned records: {transformed_df.count()}")

        print("\nTransformed data:")
        transformed_df.orderBy("order_id").show(
            truncate=False
        )

        summary_df = build_regional_summary(
            transformed_df
        )

        print("\nRegional sales summary:")
        summary_df.show(truncate=False)

        detail_output = OUTPUT_DIR / "sales"
        summary_output = OUTPUT_DIR / "regional_summary"

        (
            transformed_df.write
            .mode("overwrite")
            .partitionBy("region")
            .parquet(str(detail_output))
        )

        (
            summary_df.write
            .mode("overwrite")
            .parquet(str(summary_output))
        )

        print("\nLocal ETL test completed successfully.")
        print(f"Detailed output: {detail_output}")
        print(f"Summary output: {summary_output}")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
