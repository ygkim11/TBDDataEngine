import socketio
import json
from db import s, KiwoomStock, KiwoomFutures

sio = socketio.Client()
sio.connect('http://localhost:3001')

@sio.on('kiwoom_kospi_a_stocks')
def on_receive_kiwoom_kospi_a_stocks_data(data):
    data = json.loads(data['data'].decode('utf-8'))
    s.execute(KiwoomStock.__table__.insert(), data)
    s.commit()