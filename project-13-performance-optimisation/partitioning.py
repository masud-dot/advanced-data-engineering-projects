partition_sizes=df.rdd.mapPartitions(lambda p:[sum(1 for _ in p)]).collect()
print(f'Max: {max(partition_sizes):,} | Min: {min(partition_sizes):,} | Skew ratio: {max(partition_sizes)/min(partition_sizes):.1f}x')
df_balanced=df.repartition(16,'region'); df_balanced.coalesce(4).write.mode('overwrite').parquet('output/')
