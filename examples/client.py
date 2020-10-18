import socketio

sio = socketio.Client()
sio.connect('http://localhost:3000')

@sio.on('connect')
def connect():
    sio.emit('ready')

@sio.on('data')
def on_receive_data(data):
    print(data)