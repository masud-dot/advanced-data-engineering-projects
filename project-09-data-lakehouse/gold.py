from pyspark.sql.functions import sum as spark_sum,count,avg
silver_df=spark.read.parquet('s3://enterprise-lakehouse/silver/')
gold_df=silver_df.groupBy('product_id').agg(spark_sum('amount').alias('total_sales'),count('transaction_id').alias('order_count'),avg('amount').alias('avg_order_value'))
gold_df.write.mode('overwrite').parquet('s3://enterprise-lakehouse/gold/')
