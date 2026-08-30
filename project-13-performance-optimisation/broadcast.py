from pyspark.sql.functions import broadcast
product_lookup=spark.read.parquet('s3://data-lake/products/')
fact_sales=spark.read.parquet('s3://data-lake/sales/')
result=fact_sales.join(broadcast(product_lookup),'product_id')
spark.conf.set('spark.sql.autoBroadcastJoinThreshold',str(100*1024*1024))
