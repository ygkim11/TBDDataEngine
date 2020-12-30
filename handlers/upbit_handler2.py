import os
import time
import json
import socketio
import psycopg2
import sqlalchemy.pool as pool
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from db import KiwoomStock, KiwoomFutures, UpbitCoin

from contextlib import contextmanager

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

def getconn():
    db_conn = psycopg2.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, dbname=DB_NAME)
    return db_conn

db_pool = pool.QueuePool(getconn, max_overflow=20, pool_size=20)

db_string = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
db = create_engine(db_string, pool=db_pool)
session = scoped_session(sessionmaker(bind=db))

sio = socketio.Client()
sio.connect('http://localhost:3000')

coins_bulk_data = []
coins_start = time.time()

@sio.on('upbit')
def on_receive_upbit_data(data):
    global coins_bulk_data, coins_start
    data = json.loads(data['data'].decode('utf-8'))
    data['my_timestamp'] = str(data['my_timestamp'])
    data['timestamp'] = str(data['timestamp'])
    data['trade_timestamp'] = str(data['trade_timestamp'])
    data['hoga_timestamp'] = str(data['hoga_timestamp'])
    coins_bulk_data.append(UpbitCoin(**data))
    if time.time() - coins_start > 10.0:
        coins_start = time.time()
        save_upbit_data()

def save_upbit_data():
    global coins_bulk_data, session
    session.bulk_save_objects(coins_bulk_data)
    session.commit()
    coins_bulk_data = []