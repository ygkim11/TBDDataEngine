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
sio.connect('http://localhost:3001')

stocks_bulk_data = []
futures_bulk_data = []

stocks_start = time.time()
futures_start = time.time()

@sio.on('kiwoom_stocks')
def on_receive_kiwoom_stocks_data(data):
    global stocks_bulk_data, stocks_start
    data = json.loads(data['data'].decode('utf-8'))
    stocks_bulk_data.append(KiwoomStock(**data))
    if time.time() - stocks_start > 10.0:
        stocks_start = time.time()
        save_kiwoom_stocks_data()

@sio.on('kiwoom_futures')
def on_receive_kiwoom_futures_data(data):
    global futures_bulk_data, futures_start
    data = json.loads(data['data'].decode('utf-8'))
    futures_bulk_data.append(KiwoomFutures(**data))
    if time.time() - futures_start > 10.0:
        futures_start = time.time()
        save_kiwoom_futures_data()

def save_kiwoom_stocks_data():
    global stocks_bulk_data, session
    session.bulk_save_objects(stocks_bulk_data)
    session.commit()
    stocks_bulk_data = []

def save_kiwoom_futures_data():
    global futures_bulk_data, session
    session.bulk_save_objects(futures_bulk_data)
    session.commit()
    futures_bulk_data = []