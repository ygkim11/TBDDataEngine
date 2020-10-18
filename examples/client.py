import socketio
import Handler

sio = socketio.Client()
sio.connect('http://localhost:3000')

@sio.on('connect')
def connect():
    print('socket connected sending ready')
    sio.emit('ready', {})

@sio.on('data')
def on_receive_data(data):
    Handler.resolve(data, sio)



class Handler:
    def __init__(self):
        pass

    def resolve(data, sio):
        buy = buysignal(data)
        if buy:
            sio.emit('order', {'amount': 2})