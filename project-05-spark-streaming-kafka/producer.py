from kafka import KafkaProducer
import json, time, random
producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
cities=['Mumbai','Delhi','Bangalore','Chennai']
while True:
    event={'order_id':random.randint(1000,9999),'city':random.choice(cities),'amount':random.randint(200,1500)}
    producer.send('delivery_topic', value=event)
    time.sleep(1)
