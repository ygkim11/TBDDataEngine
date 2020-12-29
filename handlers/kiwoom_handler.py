import os
import socketio
import json
import csv
import datetime

sio = socketio.Client()
sio.connect('http://localhost:3001')

@sio.on('kiwoom_stocks')
def on_receive_kiwoom_stocks_data(data):
    data = json.loads(data)
    print(data.get('trade_date'), data.get('timestamp'), data.get('hoga_date'))

@sio.on('kiwoom_futures')
def on_receive_kiwoom_futures_data(data):
    data = json.loads(data)
    print(data.get('trade_date'), data.get('timestamp'), data.get('hoga_date'))