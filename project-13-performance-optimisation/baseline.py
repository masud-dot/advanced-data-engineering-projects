import time
from pyspark.sql import SparkSession
spark=SparkSession.builder.appName('performance_optimisation').config('spark.sql.shuffle.partitions','200').getOrCreate()
start=time.time(); df=spark.read.parquet('s3://data-lake/sales/'); count=df.count()
print(f'Rows: {count:,} | Time: {time.time()-start:.1f}s | Partitions: {df.rdd.getNumPartitions()}')
