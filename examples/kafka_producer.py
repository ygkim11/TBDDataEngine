import websocket
import ssl
from kafka import KafkaProducer
from json import dumps
import time
    
# 카프카 서버
bootstrap_servers = ["localhost:9092"]

# 카프카 공급자 생성
producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                         key_serializer=None,
                         value_serializer=lambda x: dumps(x).encode('utf-8'))

# 카프카 토픽
str_topic_name = 'testBlockchain'

def collect_data():
    uri = 'wss://ws.blockchain.info/inv'
    ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
    ws.connect(uri)

    ws.send(dumps({"op": "unconfirmed_sub"}))

    while True:
        blockchain_data = ws.recv()
        print(blockchain_data)

        # 카프카 공급자 토픽에 데이터를 보낸다
        producer.send(str_topic_name, value=blockchain_data)
        print('data:', blockchain_data)

collect_data()