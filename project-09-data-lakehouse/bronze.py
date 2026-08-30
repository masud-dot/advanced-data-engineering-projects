raw_df=spark.read.json('s3://raw-transactions/')
raw_df.write.mode('append').partitionBy('year','month','day').parquet('s3://enterprise-lakehouse/bronze/')
