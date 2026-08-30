from pyspark.sql.functions import col,count,isnull
null_counts=spark_df.select([count(isnull(c)).alias(c) for c in ['transaction_id','customer_id','amount']]).collect()[0].asDict()
invalid_amounts=spark_df.filter(col('amount')<=0)
print(f'Invalid amounts: {invalid_amounts.count():,}')
from pyspark.sql.functions import count as cnt
dupes=spark_df.groupBy('transaction_id').agg(cnt('*').alias('n')).filter(col('n')>1)
