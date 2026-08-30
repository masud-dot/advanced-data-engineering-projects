from sqlalchemy import create_engine
import pandas as pd
def ingest_orders_db(connection_string):
    engine=create_engine(connection_string); return pd.read_sql('SELECT order_id,cust_id,amount,order_date FROM orders',engine)
