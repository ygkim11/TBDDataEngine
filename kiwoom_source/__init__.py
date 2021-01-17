import os
import sys
import json
import pika
from PyQt5.QtWidgets import *
from pykafka import KafkaClient

from kiwoom.get_real_data import *
from kiwoom.process import *

from dotenv import load_dotenv

load_dotenv()

RABBIT_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBIT_PORT = os.getenv('RABBITMQ_PORT', 'localhost')
RABBIT_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBIT_PASS = os.getenv('RABBITMQ_PASSWORD', 'guest')

# rabbit_uri = f'amqp://{RABBIT_USER}:{RABBIT_PASS}@{RABBIT_HOST}:{RABBIT_PORT}/%2F'
# parameters = pika.URLParameters(rabbit_uri)

def worker(id, q):
    print(f'Started worker process {id}')
    client = KafkaClient(hosts='127.0.0.1:9092')
    topic = client.topics['kiwoom-data']
    producer = topic.get_producer(delivery_reports=False)

    while True:
        val = q.get()
        if val == 'DONE':
            break
        routing_key = val['routing_key']
        producer.produce(json.dumps(val), partition_key=routing_key)

    # credentials = pika.PlainCredentials(username=RABBIT_USER, password=RABBIT_PASS)
    # connection = pika.BlockingConnection(
    #     pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT, credentials=credentials))
    # channel = connection.channel()
    # channel.exchange_declare(exchange='kiwoom', exchange_type='topic')
    # print(f'Started RabbitMQ publisher #{id}')
    #
    # while True:
    #     val = q.get()
    #     if val == 'DONE':
    #         break
    #     routing_key = val['routing_key']
    #     del val['routing_key']
    #     channel.basic_publish(exchange='kiwoom', routing_key=routing_key, body=json.dumps(val))
    # connection.close()

class Main():
    def __init__(self, queues, processes):
        print('실행할 메인 클래스')
        self.app = QApplication(sys.argv)
        self.get_real_data = Get_Real_Data(queues, processes)
        self.app.exec_()


if __name__ == '__main__':
    p_cnt = 3
    q = create_queues(p_cnt)
    p = create_processes(q, worker)
    start_processes(p)

    Main(q, p)


