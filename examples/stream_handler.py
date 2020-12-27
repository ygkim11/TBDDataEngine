import socketio
import json
import csv

sio = socketio.Client()
sio.connect('http://localhost:3000')

@sio.on('upbit')
def on_receive_upbit_data(data):
    json_data = json.loads(data['data'].decode('utf-8'))
    with open('upbit.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow()
        data = [
            json_data['code'],
            json_data['date'],
            json_data['time'],
            json_data['my_timestamp'],
            json_data['timestamp'],
            json_data['trade_timestamp'],
            json_data['trade_price'],
            json_data['trade_volume'],
            json_data['hoga_timestamp'],
            json_data['total_ask_size'],
            json_data['total_bid_size'],
            json_data['sell_hoga15'],
            json_data['sell_hoga14'],
            json_data['sell_hoga13'],
            json_data['sell_hoga12'],
            json_data['sell_hoga11'],
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
            json_data['buy_hoga11'],
            json_data['buy_hoga12'],
            json_data['buy_hoga13'],
            json_data['buy_hoga14'],
            json_data['buy_hoga15'],
            json_data['sell_hoga15_stack'],
            json_data['sell_hoga14_stack'],
            json_data['sell_hoga13_stack'],
            json_data['sell_hoga12_stack'],
            json_data['sell_hoga11_stack'],
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
            json_data['buy_hoga11_stack'],
            json_data['buy_hoga12_stack'],
            json_data['buy_hoga13_stack'],
            json_data['buy_hoga14_stack'],
            json_data['buy_hoga15_stack']
        ]


# if __name__ == '__main__':
#     sio.emit('ready', {})