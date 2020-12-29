import socketio
import json
from db import s, KiwoomStock, KiwoomFutures

sio = socketio.Client()
sio.connect('http://localhost:3001')

@sio.on('kiwoom_futures')
def on_receive_kiwoom_futures_stocks_data(data):
    data = json.loads(data['data'].decode('utf-8'))
    s.execute(KiwoomFutures.__table__.insert(), data)
    s.commit()