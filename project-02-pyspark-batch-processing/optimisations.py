from pyspark.sql.functions import broadcast

def optimise(large_df, small_lookup_df):
    df = large_df.select('region','product_name','total_amount')
    df.cache()
    return large_df.join(broadcast(small_lookup_df), 'product_id')
