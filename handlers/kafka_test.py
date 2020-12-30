from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], compression_type='gzip')

for i in range(10):
    producer.send('test', f'hello {i}'.encode('utf-8'))
    print(i)