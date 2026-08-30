null_counts={c:silver_df.filter(col(c).isNull()).count() for c in silver_df.columns}
total=silver_df.count(); unique=silver_df.select('transaction_id').distinct().count(); assert total==unique
invalid=silver_df.filter(col('amount')<=0).count(); assert invalid==0
print('All Silver quality checks passed.')
