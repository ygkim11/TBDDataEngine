from kafka import KafkaConsumer
from json import loads

# 카프카 서버
bootstrap_servers = ["localhost:9092"]

# 카프카 토픽
str_topic_name    = 'testBlockchain'

consumer = KafkaConsumer(str_topic_name,
                         bootstrap_servers=bootstrap_servers,
                         auto_offset_reset='earliest', # 가장 처음부터 소비
                         group_id=None
                        )

print(consumer)

for message in consumer:
    print(message)