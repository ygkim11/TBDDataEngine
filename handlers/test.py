import os
import psycopg2
import sqlalchemy.pool as pool
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from db import KiwoomStock, KiwoomFutures
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
print(session)

session.bulk_save_objects([KiwoomStock(**{'code': 'aaaa'})])
session.commit()

print('done')