import socketio
import time
sio = socketio.Client()
chat_data_queue = None


@sio.event
def connect():
    print("I'm connected!")
    sio.emit('req')


@sio.on('chat_data')
def on_message(dat):
    global chat_data_queue
    if dat != 'None':
        # print(f'Data Received: {dat}')
        chat_data_queue['queueue'].put(dat)
    try:
        req = chat_data_queue['request_export'].get(0)
        if 'insults' in req:
            for i in range(0,req['insults']):
                # print('requesting Insult')
                sio.emit('insult')
                time.sleep(.02)
        if 'bbb' in req:
            sio.emit('bbb',req['bbb'])


    except:
        pass
    sio.emit('req')

@sio.on('insult')
def on_message(dat):
    # print('Insult received')

    chat_data_queue['request_import'].put(dat)



@sio.event
def connect_error(sid):
    print("The connection failed!")


@sio.event
def disconnect():
    print("I'm disconnected!")


def run_client_socket(q,ip='http://192.168.1.31:3333'):
    global chat_data_queue
    chat_data_queue = q
    sio.connect(ip)


if __name__ == '__main__':
    sio.connect('http://192.168.1.20:3333')
