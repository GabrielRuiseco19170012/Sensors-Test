import json
import time
import websocket
from threading import Thread
from DHT import DHT
from Sensors import Sensors
from File import File
from MySQL import *
from MongoDB import *
import sys
import serial

newSQL = MySQL()
newMongo = MongoDB()
newSQL.Conexion()
newMongo.mongoConexion()



# sensors = Sensors()
# sensorList = sensors.getAllInstance()
# print(sensorList)
# sensorList.returnData()


def on_message(ws, message):
    print("*" * 20)
    response = json.loads(message)
    print(response)
    value = response['d']
    if 'data' in value:
        result = value['data']
        print(result)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")
    pass


def on_open(ws):
    def run():
        # Esta información camibara dependiendo del canal a subscribir.
        subscribe = {"t": 1, "d": {"topic": "measures"}}
        ws.send(json.dumps(subscribe))
        while True:
            # Esta linea se puede borrar solamente es para mandar un mensaje a modo de ejemplo
            print("Escribe un mensaje: ")
            # Tambien este input es solo para guardar el valor del mensaje
            message = input()
            # Estos datos cambiar  dependiendo del evento e información a mandar.
            data = {"t": 7, "d": {"topic": "measures", "event": "message", "data": message}}
            ws.send(json.dumps(data))
            time.sleep(3)

    Thread(target=run).start()

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    ser.flush()

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)

# if __name__ == "__main__":
#     websocket.enableTrace(True)
#     uri = "ws://chat-api-for-python-v0.herokuapp.com/adonis-ws"
#     ws = websocket.WebSocketApp(uri,
#                                 on_open=on_open,
#                                 on_message=on_message,
#                                 on_error=on_error,
#                                 on_close=on_close,
#                                 )
#     ws.run_forever()
