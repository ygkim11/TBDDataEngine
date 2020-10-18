import websocket
import ssl
from kafka import KafkaProducer
from json import dumps
import time
from random import randrange
    
# 카프카 서버
bootstrap_servers = ["localhost:9092"]

# 카프카 공급자 생성
producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                         key_serializer=None,
                         value_serializer=lambda x: dumps(x).encode('utf-8'))

# 카프카 토픽
str_topic_name = 'kiwoom'

def send_data():
    test_data = [
        '000010,1,1,1,1',
        '000020,2,2,2,2',
        '000030,3,3,3,3',
        '000040,4,4,4,4'
    ]

    while True:
        time.sleep(3)
        rand_idx = randrange(4)
        producer.send(str_topic_name, value=test_data[rand_idx])
        print('data:', test_data[rand_idx])

send_data()