from pyspark.sql.functions import col,concat,lit,rand
df.groupBy('region').count().orderBy('count',ascending=False).show()
SALT_FACTOR=8
salted_df=skewed_df.withColumn('salted_key',concat(col('region'),lit('_'),(rand()*SALT_FACTOR).cast('int')))
spark.conf.set('spark.sql.adaptive.enabled','true'); spark.conf.set('spark.sql.adaptive.skewJoin.enabled','true')
