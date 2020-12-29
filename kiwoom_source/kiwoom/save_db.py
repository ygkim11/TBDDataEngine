from kiwoom.db import s, KiwoomStock, KiwoomFutures

def save_kiwoom_stocks_data_to_db(data):
    json_data = json.loads(data)
    s.execute(KiwoomStock.__table__.insert(), json_data)
    s.commit()

def save_kiwoom_futures_data_to_db(data):
    json_data = json.loads(data)
    s.execute(KiwoomFutures.__table__.insert(), json_data)
    s.commit()