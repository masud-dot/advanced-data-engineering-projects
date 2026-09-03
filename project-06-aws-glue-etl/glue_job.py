import logging
import os
import sys
from datetime import datetime

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, current_timestamp, sum as spark_sum
from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

DEFAULT_SOURCE_PATH = os.getenv(
    "SOURCE_PATH",
    "s3://enterprise-etl-bucket/raw/sales_data/",
)
DEFAULT_OUTPUT_PATH = os.getenv(
    "OUTPUT_PATH",
    "s3://enterprise-etl-bucket/processed/sales/",
)
DEFAULT_SUMMARY_PATH = os.getenv(
    "SUMMARY_PATH",
    "s3://enterprise-etl-bucket/processed/regional_summary/",
)
DEFAULT_DATABASE = os.getenv("GLUE_DATABASE", "enterprise_db")
DEFAULT_TABLE = os.getenv("GLUE_TABLE", "sales_data")

SALES_SCHEMA = StructType(
    [
        StructField("order_id", IntegerType(), False),
        StructField("customer_id", IntegerType(), False),
        StructField("region", StringType(), False),
        StructField("product", StringType(), False),
        StructField("quantity", IntegerType(), False),
        StructField("price", DoubleType(), False),
        StructField("order_date", StringType(), True),
    ]
)


def create_glue_context():
    """Create Spark and AWS Glue contexts."""
    sc = SparkContext.getOrCreate()
    glue_context = GlueContext(sc)
    spark = glue_context.spark_session

    spark.conf.set("spark.sql.session.timeZone", "UTC")

    return sc, glue_context, spark


def read_from_catalog(
    glue_context: GlueContext,
    database: str,
    table: str,
) -> DataFrame:
    """Read source data through the AWS Glue Data Catalog."""
    LOGGER.info(
        "Reading Glue Catalog table: database=%s, table=%s",
        database,
        table,
    )

    dynamic_frame = (
        glue_context.create_dynamic_frame.from_catalog(
            database=database,
            table_name=table,
            transformation_ctx="source_catalog",
        )
    )

    return dynamic_frame.toDF()


def clean_and_transform(df: DataFrame) -> DataFrame:
    """Clean source records and calculate transaction totals."""
    LOGGER.info("Starting data cleaning and transformation.")

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

    transformed_df = (
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

    LOGGER.info("Cleaning and transformation completed.")

    return transformed_df


def build_regional_summary(df: DataFrame) -> DataFrame:
    """Aggregate sales by region."""
    LOGGER.info("Building regional sales summary.")

    return (
        df.groupBy("region")
        .agg(
            spark_sum("total_amount").alias("regional_sales")
        )
        .orderBy("region")
    )


def write_partitioned_parquet(
    df: DataFrame,
    output_path: str,
) -> None:
    """Write detailed records as partitioned Parquet files."""
    LOGGER.info(
        "Writing detailed data to: %s",
        output_path,
    )

    (
        df.write
        .mode("overwrite")
        .partitionBy("region")
        .parquet(output_path)
    )

    LOGGER.info("Detailed Parquet output completed.")


def write_summary_parquet(
    df: DataFrame,
    output_path: str,
) -> None:
    """Write regional aggregation as Parquet."""
    LOGGER.info(
        "Writing regional summary to: %s",
        output_path,
    )

    (
        df.write
        .mode("overwrite")
        .parquet(output_path)
    )

    LOGGER.info("Regional summary output completed.")


def resolve_job_arguments():
    """Resolve AWS Glue job arguments."""
    required_arguments = [
        "JOB_NAME",
    ]

    optional_arguments = [
        "SOURCE_PATH",
        "OUTPUT_PATH",
        "SUMMARY_PATH",
        "GLUE_DATABASE",
        "GLUE_TABLE",
    ]

    available_arguments = required_arguments + optional_arguments

    try:
        args = getResolvedOptions(
            sys.argv,
            available_arguments,
        )
    except Exception:
        args = getResolvedOptions(
            sys.argv,
            required_arguments,
        )

    return {
        "job_name": args["JOB_NAME"],
        "source_path": args.get(
            "SOURCE_PATH",
            DEFAULT_SOURCE_PATH,
        ),
        "output_path": args.get(
            "OUTPUT_PATH",
            DEFAULT_OUTPUT_PATH,
        ),
        "summary_path": args.get(
            "SUMMARY_PATH",
            DEFAULT_SUMMARY_PATH,
        ),
        "database": args.get(
            "GLUE_DATABASE",
            DEFAULT_DATABASE,
        ),
        "table": args.get(
            "GLUE_TABLE",
            DEFAULT_TABLE,
        ),
    }


def main():
    """Run the AWS Glue ETL pipeline."""
    args = resolve_job_arguments()

    LOGGER.info("Starting AWS Glue ETL job: %s", args["job_name"])
    LOGGER.info("Job started at: %s UTC", datetime.utcnow())

    sc, glue_context, spark = create_glue_context()

    job = Job(glue_context)
    job.init(args["job_name"], args)

    try:
        source_df = read_from_catalog(
            glue_context,
            args["database"],
            args["table"],
        )

        LOGGER.info(
            "Source columns: %s",
            source_df.columns,
        )

        cleaned_df = clean_and_transform(source_df)

        regional_summary_df = build_regional_summary(
            cleaned_df
        )

        write_partitioned_parquet(
            cleaned_df,
            args["output_path"],
        )

        write_summary_parquet(
            regional_summary_df,
            args["summary_path"],
        )

        job.commit()

        LOGGER.info(
            "AWS Glue ETL job completed successfully."
        )

    except Exception:
        LOGGER.exception(
            "AWS Glue ETL job failed."
        )
        raise

    finally:
        spark.stop()


if __name__ == "__main__":
    main()
