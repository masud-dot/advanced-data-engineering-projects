stream_df=spark.readStream.format('kafka').option('kafka.bootstrap.servers','kafka:9092').option('subscribe','payment_events').load()
from pyspark.sql.functions import from_json,col,current_timestamp,window,sum as s
from pyspark.sql.types import StructType,StructField,StringType,DoubleType
schema=StructType([StructField('customer_id',StringType()),StructField('amount',DoubleType()),StructField('event_type',StringType())])
parsed=stream_df.selectExpr('CAST(value AS STRING)').select(from_json(col('value'),schema).alias('d')).select('d.*').withColumn('ts',current_timestamp())
live_revenue=parsed.withWatermark('ts','1 minute').groupBy(window('ts','5 minutes')).agg(s('amount').alias('revenue'))
live_revenue.writeStream.format('console').outputMode('update').start()
