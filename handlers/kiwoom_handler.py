import os
import socketio
import json
import csv
import datetime

sio = socketio.Client()
sio.connect('http://localhost:3000')

stocks_drive_location = 'C:\\Users\\simpl\\real_time_data\\kiwoom_stocks\\'
futures_drive_location = 'C:\\Users\\simpl\\real_time_data\\kiwoom_futures\\'

@sio.on('kiwoom_stocks')
def on_receive_kiwoom_stocks_data(data):
    today = datetime.datetime.now()
    folder_name = today.strftime('%Y-%m-%d')
    file_name = today.strftime('%Y-%m-%d_%H')
    dirname = f'{stocks_drive_location}\\{folder_name}'
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    file_location = f'{dirname}\\{file_name}.csv'
    json_data = json.loads(data['data'].decode('utf-8'))
    with open(file_location, 'a', newline='') as f:
        writer = csv.writer(f)
        data = [
            json_data['code'],
            json_data['date'],
            json_data['current_price'],
            json_data['open_price'],
            json_data['high'],
            json_data['low'],
            json_data['volume'],
            json_data['cum_volume'],
            json_data['trade_sell_hoga1'],
            json_data['trade_buy_hoga1'],
            json_data['hoga_date'],
            json_data['sell_hoga10'],
            json_data['sell_hoga9'],
            json_data['sell_hoga8'],
            json_data['sell_hoga7'],
            json_data['sell_hoga6'],
            json_data['sell_hoga5'],
            json_data['sell_hoga4'],
            json_data['sell_hoga3'],
            json_data['sell_hoga2'],
            json_data['sell_hoga1'],
            json_data['buy_hoga1'],
            json_data['buy_hoga2'],
            json_data['buy_hoga3'],
            json_data['buy_hoga4'],
            json_data['buy_hoga5'],
            json_data['buy_hoga6'],
            json_data['buy_hoga7'],
            json_data['buy_hoga8'],
            json_data['buy_hoga9'],
            json_data['buy_hoga10'],
            json_data['sell_hoga10_stack'],
            json_data['sell_hoga9_stack'],
            json_data['sell_hoga8_stack'],
            json_data['sell_hoga7_stack'],
            json_data['sell_hoga6_stack'],
            json_data['sell_hoga5_stack'],
            json_data['sell_hoga4_stack'],
            json_data['sell_hoga3_stack'],
            json_data['sell_hoga2_stack'],
            json_data['sell_hoga1_stack'],
            json_data['buy_hoga1_stack'],
            json_data['buy_hoga2_stack'],
            json_data['buy_hoga3_stack'],
            json_data['buy_hoga4_stack'],
            json_data['buy_hoga5_stack'],
            json_data['buy_hoga6_stack'],
            json_data['buy_hoga7_stack'],
            json_data['buy_hoga8_stack'],
            json_data['buy_hoga9_stack'],
            json_data['buy_hoga10_stack'],
            json_data['total_buy_hoga_stack'],
            json_data['total_sell_hoga_stack'],
            json_data['net_buy_hoga_stack'],
            json_data['net_sell_hoga_stack'],
            json_data['ratio_buy_hoga_stack'],
            json_data['ratio_sell_hoga_stack']
        ]
        writer.writerow(data)


@sio.on('kiwoom_futures')
def on_receive_kiwoom_futures_data(data):
    today = datetime.datetime.now()
    folder_name = today.strftime('%Y-%m-%d')
    file_name = today.strftime('%Y-%m-%d_%H')
    dirname = f'{futures_drive_location}\\{folder_name}'
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    file_location = f'{dirname}\\{file_name}.csv'
    json_data = json.loads(data['data'].decode('utf-8'))
    with open(file_location, 'a', newline='') as f:
        writer = csv.writer(f)
        data = [
            json_data['code'],
            json_data['date'],
            json_data['current_price'],
            json_data['open_price'],
            json_data['high'],
            json_data['low'],
            json_data['volume'],
            json_data['cum_volume'],
            json_data['trade_sell_hoga1'],
            json_data['trade_buy_hoga1'],
            json_data['hoga_date'],
            json_data['sell_hoga10'],
            json_data['sell_hoga9'],
            json_data['sell_hoga8'],
            json_data['sell_hoga7'],
            json_data['sell_hoga6'],
            json_data['sell_hoga5'],
            json_data['sell_hoga4'],
            json_data['sell_hoga3'],
            json_data['sell_hoga2'],
            json_data['sell_hoga1'],
            json_data['buy_hoga1'],
            json_data['buy_hoga2'],
            json_data['buy_hoga3'],
            json_data['buy_hoga4'],
            json_data['buy_hoga5'],
            json_data['buy_hoga6'],
            json_data['buy_hoga7'],
            json_data['buy_hoga8'],
            json_data['buy_hoga9'],
            json_data['buy_hoga10'],
            json_data['sell_hoga10_stack'],
            json_data['sell_hoga9_stack'],
            json_data['sell_hoga8_stack'],
            json_data['sell_hoga7_stack'],
            json_data['sell_hoga6_stack'],
            json_data['sell_hoga5_stack'],
            json_data['sell_hoga4_stack'],
            json_data['sell_hoga3_stack'],
            json_data['sell_hoga2_stack'],
            json_data['sell_hoga1_stack'],
            json_data['buy_hoga1_stack'],
            json_data['buy_hoga2_stack'],
            json_data['buy_hoga3_stack'],
            json_data['buy_hoga4_stack'],
            json_data['buy_hoga5_stack'],
            json_data['buy_hoga6_stack'],
            json_data['buy_hoga7_stack'],
            json_data['buy_hoga8_stack'],
            json_data['buy_hoga9_stack'],
            json_data['buy_hoga10_stack'],
            json_data['total_buy_hoga_stack'],
            json_data['total_sell_hoga_stack'],
            json_data['net_buy_hoga_stack'],
            json_data['net_sell_hoga_stack'],
            json_data['ratio_buy_hoga_stack'],
            json_data['ratio_sell_hoga_stack']
        ]
        writer.writerow(data)