from pyspark.sql.functions import sum as s,count
silver_df=spark.read.parquet('s3://enterprise-platform/silver/')
daily_summary=silver_df.groupBy('sale_date','region','product_id').agg(s('amount').alias('total_revenue'),count('transaction_id').alias('order_count'))
daily_summary.write.mode('overwrite').partitionBy('sale_date').parquet('s3://enterprise-platform/gold/')
