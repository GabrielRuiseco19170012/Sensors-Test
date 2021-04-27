import json
import time
import websocket
import threading
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
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
pinRegar = 18
pinLuz = 17
sensors = Sensors()
sensorList = sensors.getAllInstance()
sensors.readThread()

# print(sensorList)
# sensorList.returnData()


def on_message(ws, message):
    print("*" * 20)
    response = json.loads(message)
    print(response)
    value = response['d']
    if 'data' in value:
        result = value['data']
        if result['plantID'] == sensors.id:
            if result['order'] == "regar":
                GPIO.output(pinRegar, GPIO.HIGH)
                time.sleep(5)
                GPIO.output(pinRegar, GPIO.LOW)
            if result['order'] == "iluminar":
                if GPIO.input(pinLuz) == 0:
                    GPIO.output(pinLuz, GPIO.HIGH)
                elif GPIO.input(pinLuz) == 1:
                    GPIO.output(pinLuz, GPIO.LOW)


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
            sensor.
            data = {"t": 7, "d": {"topic": "measures", "event": "message", "data": message}}
            ws.send(json.dumps(data))
            time.sleep(3)

    threading.Thread(target=run).start()


def send_data():
    while True:
        try:
            sensor = sensors.getOneInstance('DHT-11')
            ws.send('{"t":7,"d":{"topic":"measures","event":"message","data":{"temperature":' + str(
                sensor.temperature) + ', "humidity":' + str(sensor.humidity) + '}}}')
        except RuntimeError:
            pass


if __name__ == "__main__":
    websocket.enableTrace(True)
    uri = "ws://api-smart-garden.herokuapp.com/adonis-ws"
    ws = websocket.WebSocketApp(uri,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                )
    ws.run_forever()
