from kafka import KafkaConsumer
from kafka.structs import TopicPartition
import json
import datetime
import time

def string_to_timestamp(string_date):
    t = datetime.datetime.strptime(string_date, '%Y-%m-%d %H:%M:%S')
    return int(time.mktime(t.timetuple()) * 1000)

def timestamp_to_string(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp / 1000)
    return dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

class Kafka:
    def __init__(self, topic):
        deserializer = lambda x: json.loads(x.decode('utf-8'))

        self.topic = topic

        self.consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'],
                                      auto_offset_reset='earliest',
                                      # value_deserializer=deserializer,
                                      consumer_timeout_ms=1000)
        self.change_topic(topic)

    def __iter__(self):
        return self.consumer

    def __len__(self):
        offset = self.get_offset()
        self.set_offset_to_end()
        full_len = self.get_offset()
        self.set_offset(offset)
        return full_len

    def next(self):
        return next(self.consumer)

    def get_topics(self):
        print(self.consumer.topics())

    def change_topic(self, topic):
        self.partition = TopicPartition(topic, 0)
        self.consumer.assign([self.partition])

    def set_offset_to_start(self):
        self.consumer.seek_to_beginning(self.partition)

    def set_offset_to_end(self):
        self.consumer.seek_to_end(self.partition)

    def set_offset(self, offset: int):
        self.consumer.seek(self.partition, offset)

    def get_offset(self):
        return self.consumer.position(self.partition)

    def set_offset_for_time(self, time_string):
        offset = self.get_offset_for_time(time_string)
        if isinstance(offset, type(None)):
            self.set_offset_to_end()
        else:
            self.set_offset(offset.offset)

    def get_offset_for_time(self, time_string):
        ts = string_to_timestamp(time_string)
        return list(self.consumer.offsets_for_times({self.partition: ts}).values())[0]


kafka = Kafka('kiwoom_stocks')
kafka.set_offset_to_start()

# kafka.change_topic('my_topic')
# kafka.set_offset_for_time('2020-12-31 11:59:07')

kafka.set_offset(1300201)

for i in range(10):
    print(kafka.next())

print(len(kafka))