from kafka import KafkaProducer
import json, time

producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
orders = [
    {'order_id':1001,'customer':'Alice','product':'Laptop','amount':75000},
    {'order_id':1002,'customer':'Bob','product':'Keyboard','amount':2000},
]
for order in orders:
    producer.send('orders_topic', value=order)
    print(f'Published: {order}')
    time.sleep(1)
producer.flush()
