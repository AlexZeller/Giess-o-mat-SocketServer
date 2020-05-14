from giessomat import Relais
from giessomat import Fans
import eventlet
import socketio


eventlet.monkey_patch()

relais_light = Relais.Relais(23)
relais_fan = Relais.Relais(24)
relais_pump = Relais.Relais(25)
relais_valve = Relais.Relais(16)

mgr = socketio.KombuManager('amqp://')
sio = socketio.Server(cors_allowed_origins=[
                      'http://localhost:5672', 'http://192.168.0.134:8080', 'http://192.168.0.235'], client_manager=mgr)

app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print('Client connect', sid)


@sio.event
def light(sid, data):
    if data == True:
        print(data)
        sio.emit('light', True)
        relais_light.on()
    if data == False:
        print(data)
        sio.emit('light', False)
        relais_light.off()
    if data == 'status:
        print('Status request')


@sio.event
def fan(sid, data):
    if data == True:
        print(data)
        sio.emit('fan', True)
        relais_fan.on()
    if data == False:
        print(data)
        sio.emit('fan', False)
        relais_fan.off()
    if data == 'status:
        print('Status request')


@sio.event
def irrigation(sid, data):
    if data == True:
        print(data)
        sio.emit('irrigation', True)
        relais_irrigation.on()
    if data == False:
        print(data)
        sio.emit('irrigation', False)
        relais_irrigation.off()
    if data == 'status:
        print('Status request')


@sio.event
def disconnect(sid):
    print('Client disconnect', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
