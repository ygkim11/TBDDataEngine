import socketio
import json

sio = socketio.Client()
sio.connect('http://192.168.219.100:3001')

@sio.on('kiwoom_stocks')
def kiwoom_stocks(data):
    json_data = json.loads(data['data'].decode('utf-8'))
    if json_data['code'] == '005930':
        print(json_data)