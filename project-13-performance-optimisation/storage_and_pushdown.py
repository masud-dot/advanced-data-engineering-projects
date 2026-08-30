from pyspark import StorageLevel
sales_df=spark.read.parquet('s3://data-lake/sales/'); sales_df.cache()
large_df.persist(StorageLevel.MEMORY_AND_DISK)
sales_df.unpersist()
optimised_df=spark.read.parquet('s3://data-lake/sales/').select('region','amount','sale_date').filter(col('sale_date')>='2026-01-01')
partitioned_df=spark.read.parquet('s3://data-lake/sales/').filter('year = 2026 AND month = 1')
