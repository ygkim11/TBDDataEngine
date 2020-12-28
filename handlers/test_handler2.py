import socketio
import json

sio = socketio.Client()
sio.connect('http://192.168.219.100:3000')

@sio.on('upbit')
def upbit_data(data):
    json_data = json.loads(data['data'].decode('utf-8'))
    if json_data['code'] == 'KRW-BTC':
        print(json_data)