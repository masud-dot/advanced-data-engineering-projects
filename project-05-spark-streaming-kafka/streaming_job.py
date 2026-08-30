from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark = SparkSession.builder.appName('KafkaSparkStreaming').getOrCreate()
spark.sparkContext.setLogLevel('WARN')
stream_df = spark.readStream.format('kafka').option('kafka.bootstrap.servers','localhost:9092').option('subscribe','delivery_topic').option('startingOffsets','latest').load()
schema=StructType([StructField('order_id',IntegerType()),StructField('city',StringType()),StructField('amount',IntegerType())])
parsed_df=stream_df.selectExpr('CAST(value AS STRING) AS json_str').select(from_json(col('json_str'),schema).alias('data')).select('data.*').withColumn('processing_time',current_timestamp())
windowed_sales=parsed_df.withWatermark('processing_time','1 minute').groupBy(window(col('processing_time'),'5 minutes'),col('city')).agg(sum('amount').alias('window_sales'))

def write_to_postgres(batch_df,batch_id):
    batch_df.write.format('jdbc').option('url','jdbc:postgresql://localhost:5432/data_engineering').option('dbtable','city_sales_stream').option('user','postgres').option('password','admin').mode('append').save()

query=windowed_sales.writeStream.foreachBatch(write_to_postgres).outputMode('update').option('checkpointLocation','/tmp/spark_checkpoint/').start()
query.awaitTermination()
