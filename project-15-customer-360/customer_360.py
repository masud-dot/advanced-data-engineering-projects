from pyspark.sql.functions import sum as s,count
customers=spark.read.parquet('s3://unified/customers/')
orders=spark.read.parquet('s3://unified/orders/')
events=spark.read.parquet('s3://unified/events/')
unified=customers.join(orders,'customer_id','left').join(events,'customer_id','left')
customer_360=unified.groupBy('customer_id','name','country').agg(s('amount').alias('lifetime_value'),count('order_id').alias('total_orders'),count('session').alias('total_sessions'))
customer_360.write.mode('overwrite').parquet('s3://unified/gold/customer_360/')
