from kafka_consumer import Kafka
import datetime
import json
import csv
import time

today = datetime.datetime.now().strftime('%Y-%m-%d')

def _write_to_csv(path, asset, key, value, hour, columns):
    with open(f'{path}\\{asset}_{key}_{today.replace("-", "")}_{hour}.csv', 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writerow(value)

def save_stocks_data_to_csv(time_from='083000', offset_from=0):
    kafka = Kafka('kiwoom_data')
    # offset = kafka.get_offset_for_time(f'{today} 00:00:00')
    # kafka.set_offset(offset.offset)
    total_cnt = len(kafka)

    offset = offset_from
    kafka.set_offset(offset)
    for msg in kafka:
        val = json.loads(msg.value)
        timestamp = float(val['timestamp'])
        msg_time = timestamp - (float(today.replace('-', '')) * 1000000)
        if msg_time >= float(time_from):
            break
        offset += 1

    kafka.set_offset(offset)

    cnt = 0
    orderbook_columns = None
    trade_columns = None

    for msg in kafka:
        key = msg.key.decode('utf-8')
        asset_type = key.split('.')[0]
        data_type = key.split('.')[1]
        val = msg.value
        val = json.loads(val)
        del val['routing_key']
        hour = val['timestamp'][8:10]

        if data_type == 'orderbook' and isinstance(orderbook_columns, type(None)):
            orderbook_columns = list(val.keys())

        if data_type == 'trade' and isinstance(trade_columns, type(None)):
            trade_columns = list(val.keys())

        _write_to_csv(
            f'C:\\Users\\simpl\\source\\data\\{asset_type}',
            asset_type,
            data_type,
            val,
            hour,
            orderbook_columns if data_type == 'orderbook' else trade_columns
        )
        cnt += 1
        if cnt % 10000 == 0:
            print(f'({cnt}/{total_cnt}) STOCK DONE')

def save_futures_data_to_csv():
    kafka = Kafka('kiwoom_futures')
    offset = kafka.get_offset_for_time(f'{today} 00:00:00')
    kafka.set_offset(offset.offset)
    total_cnt = len(kafka)

    cnt = 0
    orderbook_columns = None
    trade_columns = None

    for msg in kafka:
        key = msg.key.decode('utf-8')
        val = msg.value
        val = json.loads(val)
        hour = val['timestamp'][8:10]

        if key == 'orderbook' and isinstance(orderbook_columns, type(None)):
            orderbook_columns = list(val.keys())

        if key == 'trade' and isinstance(trade_columns, type(None)):
            trade_columns = list(val.keys())

        _write_to_csv(
            'C:\\Users\\simpl\\source\\data\\futures',
            'futures',
            key,
            val,
            hour,
            orderbook_columns if key == 'orderbook' else trade_columns
        )
        cnt += 1
        if cnt % 10000 == 0:
            print(f'({cnt}/{total_cnt}) FUTURES DONE')


if __name__ == '__main__':
    wday = time.localtime().tm_wday
    if wday not in [5, 6]: # 토일 제외
        save_stocks_data_to_csv(offset_from=4997521)
    #     save_futures_data_to_csv()