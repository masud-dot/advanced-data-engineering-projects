import os, json
import pandas as pd
from kafka import KafkaConsumer
from sqlalchemy import create_engine

engine = create_engine(os.getenv('DATABASE_URL','postgresql://postgres:admin@localhost:5432/data_engineering'))
consumer = KafkaConsumer('orders_topic', bootstrap_servers='localhost:9092', auto_offset_reset='earliest', group_id='order_processing_group', value_deserializer=lambda x: json.loads(x.decode('utf-8')))
for message in consumer:
    order = message.value
    pd.DataFrame([order]).to_sql('live_orders', engine, if_exists='append', index=False)
    print(f'Persisted order {order["order_id"]}')
