from pyspark.sql.functions import to_timestamp,col
bronze_df=spark.read.parquet('s3://enterprise-lakehouse/bronze/')
silver_df=bronze_df.dropDuplicates(['transaction_id']).dropna()
silver_df=silver_df.withColumn('event_time',to_timestamp('event_time')).filter(col('amount')>0).filter(col('customer_id').isNotNull())
silver_df.write.mode('overwrite').partitionBy('year','month').parquet('s3://enterprise-lakehouse/silver/')
