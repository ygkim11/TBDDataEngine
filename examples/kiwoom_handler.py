import socketio
import json
import csv
import datetime

sio = socketio.Client()
sio.connect('http://localhost:3000')

stocks_drive_location = 'C:\\Users\\simpl\\real_time_data\\kiwoom_stocks\\'
futures_drive_location = 'C:\\Users\\simpl\\real_time_data\\kiwoom_futures\\'

@sio.on('kiwoom_stocks')
def on_receive_upbit_data(data):
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    file_location = f'{stocks_drive_location}{today}.csv'
    json_data = json.loads(data['data'].decode('utf-8'))
    with open(file_location, 'a', newline='') as f:
        writer = csv.writer(f)
        data = [

        'code': None,
        'date': None,
        'current_price': None,
        'open_price': None,
        'high': None,
        'low': None,
        'volume': None,
        'cum_volume': None,
        'trade_sell_hoga1': None,
        'trade_buy_hoga1': None,
        'hoga_date': None,
        'sell_hoga10': None,
        'sell_hoga9': None,
        'sell_hoga8': None,
        'sell_hoga7': None,
        'sell_hoga6': None,
        'sell_hoga5': None,
        'sell_hoga4': None,
        'sell_hoga3': None,
        'sell_hoga2': None,
        'sell_hoga1': None,
        'buy_hoga1': None,
        'buy_hoga2': None,
        'buy_hoga3': None,
        'buy_hoga4': None,
        'buy_hoga5': None,
        'buy_hoga6': None,
        'buy_hoga7': None,
        'buy_hoga8': None,
        'buy_hoga9': None,
        'buy_hoga10': None,
        'sell_hoga10_stack': None,
        'sell_hoga9_stack': None,
        'sell_hoga8_stack': None,
        'sell_hoga7_stack': None,
        'sell_hoga6_stack': None,
        'sell_hoga5_stack': None,
        'sell_hoga4_stack': None,
        'sell_hoga3_stack': None,
        'sell_hoga2_stack': None,
        'sell_hoga1_stack': None,
        'buy_hoga1_stack': None,
        'buy_hoga2_stack': None,
        'buy_hoga3_stack': None,
        'buy_hoga4_stack': None,
        'buy_hoga5_stack': None,
        'buy_hoga6_stack': None,
        'buy_hoga7_stack': None,
        'buy_hoga8_stack': None,
        'buy_hoga9_stack': None,
        'buy_hoga10_stack': None,
        'total_buy_hoga_stack': None,
        'total_sell_hoga_stack': None,
        'net_buy_hoga_stack': None,
        'net_sell_hoga_stack': None,
        'ratio_buy_hoga_stack': None,
        'ratio_sell_hoga_stack': None
        ]
        writer.writerow(data)

# if __name__ == '__main__':
#     sio.emit('ready', {})