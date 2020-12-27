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
            sell_hoga15,
            sell_hoga14,
            sell_hoga13,
            sell_hoga12,
            sell_hoga11,
            sell_hoga10,
            sell_hoga9,
            sell_hoga8,
            sell_hoga7,
            sell_hoga6,
            sell_hoga5,
            sell_hoga4,
            sell_hoga3,
            sell_hoga2,
            sell_hoga1,
            buy_hoga1,
            buy_hoga2,
            buy_hoga3,
            buy_hoga4,
            buy_hoga5,
            buy_hoga6,
            buy_hoga7,
            buy_hoga8,
            buy_hoga9,
            buy_hoga10,
            buy_hoga11,
            buy_hoga12,
            buy_hoga13,
            buy_hoga14,
            buy_hoga15,
            sell_hoga15_stack,
            sell_hoga14_stack,
            sell_hoga13_stack,
            sell_hoga12_stack,
            sell_hoga11_stack,
            sell_hoga10_stack,
            sell_hoga9_stack,
            sell_hoga8_stack,
            sell_hoga7_stack,
            sell_hoga6_stack,
            sell_hoga5_stack,
            sell_hoga4_stack,
            sell_hoga3_stack,
            sell_hoga2_stack,
            sell_hoga1_stack,
            buy_hoga1_stack,
            buy_hoga2_stack,
            buy_hoga3_stack,
            buy_hoga4_stack,
            buy_hoga5_stack,
            buy_hoga6_stack,
            buy_hoga7_stack,
            buy_hoga8_stack,
            buy_hoga9_stack,
            buy_hoga10_stack,
            buy_hoga11_stack,
            buy_hoga12_stack,
            buy_hoga13_stack,
            buy_hoga14_stack,
            buy_hoga15_stack,
        ]


# if __name__ == '__main__':
#     sio.emit('ready', {})