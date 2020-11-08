import socketio
import json

sio = socketio.Client()
sio.connect('http://localhost:3000')

@sio.on('upbit')
def on_receive_data(data):
    json_data = json.loads(data['data'].decode('utf-8'))
    print(json_data)
    # Handler.resolve(data, sio)

if __name__ == '__main__':
    sio.emit('ready', {})


# class Handler:
#     def __init__(self):
#         pass

#     def resolve(data, sio):
#         buy = buysignal(data)
#         if buy:
#             sio.emit('order', {'amount': 2})