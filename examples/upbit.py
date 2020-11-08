import pika
import websocket
import json
import ssl
try:
    import thread
except ImportError:
    import _thread as thread
import time

conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = conn.channel()
channel.queue_declare(queue='kiwoom_data')

def make_rabbit_data(message):
    return list(message.values())

def on_message(ws, message):
    get_message = json.loads(message.decode('utf-8'))
    data = make_rabbit_data(get_message)
    json_data = json.dumps(data)
    print(json_data)
    # channel.basic_publish(exchage='',
    #                       routing_key='kiwoom_data',
    #                       body='hello')

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("close")

def on_open(ws):
    def run(*args):
        sendData = '[{"ticket":"test"},{"type":"trade","codes":["KRW-BTC","KRW-ETH"]}]'
        ws.send(sendData)
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    # ws = websocket.WebSocketApp("wss://api.upbit.com/websocket/v1",
    #                           on_message=on_message,
    #                           on_error=on_error,
    #                           on_close=on_close)
    # ws.on_open = on_open
    # ws.run_forever(sslopt={'cert_reqs': ssl.CERT_NONE})

    channel.basic_publish(exchange='', routing_key='kiwoom_data', body='hello')