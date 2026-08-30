# IAM and Cost

Pipeline roles follow least privilege: Kafka producer writes only required topics; Spark reads Bronze and writes Silver; Glue reads/writes required S3 prefixes; Redshift loads only the Gold prefix.

Use SSE-KMS for S3, TLS in transit, and appropriate Redshift encryption.

Cost levers from the book: EMR auto-scaling/spot capacity, Parquet + Snappy, partition pruning, incremental processing, and warehouse pause/resume where supported.
