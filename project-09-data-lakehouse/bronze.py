"""
Bronze layer reference implementation for Apache Spark.

Production usage:
    spark.read.json("s3://raw-transactions/") \
        .write.mode("append") \
        .partitionBy("year", "month", "day") \
        .parquet("s3://enterprise-lakehouse/bronze/")
"""


def describe_bronze_layer():
    return "Raw source data stored as Parquet in the Bronze layer."


if __name__ == "__main__":
    print(describe_bronze_layer())
