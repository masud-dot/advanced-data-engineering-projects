df.write.mode('overwrite').option('compression','snappy').partitionBy('year','month').parquet('s3://data-lake/optimised_sales/')
raw=spark.read.parquet('s3://data-lake/raw/'); raw.coalesce(10).write.mode('overwrite').parquet('s3://data-lake/compacted/')
