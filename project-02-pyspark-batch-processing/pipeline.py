from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum

spark = SparkSession.builder.appName('SalesBatchPipeline').config('spark.executor.memory','4g').config('spark.sql.shuffle.partitions','8').getOrCreate()

df = spark.read.csv('datasets/large_sales_data.csv', header=True, inferSchema=True)
df = df.withColumn('total_amount', col('quantity') * col('price')).dropna().dropDuplicates()
sales_summary = df.groupBy('region').agg(spark_sum('total_amount').alias('regional_sales'))
sales_summary.show()

df = df.repartition(8)
df = df.coalesce(4)
df.write.mode('overwrite').parquet('output/processed_sales')

sales_summary.write.format('jdbc').option('url','jdbc:postgresql://localhost:5432/data_engineering').option('dbtable','sales_summary').option('user','postgres').option('password','admin').mode('overwrite').save()
spark.stop()
