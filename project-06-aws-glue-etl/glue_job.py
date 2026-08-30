from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql.functions import col, sum as spark_sum, current_timestamp

sc=SparkContext()
glueContext=GlueContext(sc)
spark=glueContext.spark_session
job=Job(glueContext)

datasource=glueContext.create_dynamic_frame.from_catalog(database='enterprise_db',table_name='sales_data')
df=datasource.toDF().dropDuplicates().dropna()
df=df.withColumn('total_amount',col('quantity')*col('price')).withColumn('processed_time',current_timestamp())
summary_df=df.groupBy('region').agg(spark_sum('total_amount').alias('regional_sales'))
df.write.partitionBy('region').mode('overwrite').parquet('s3://enterprise-etl-bucket/processed/')
job.commit()
