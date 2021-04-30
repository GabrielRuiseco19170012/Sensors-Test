import json
import time
import websocket
import threading
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from DHT import DHT
from SerialADC import SerialADC
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
GPIO.setup(pinRegar, GPIO.OUT)
GPIO.setup(pinLuz, GPIO.OUT)
sensors = Sensors()
sensorList = sensors.getAllInstance()
# sensors.readThread()


def on_message(ws, message):
    print("*" * 20)
    print(type(message))
    response = json.loads(message)
    
    value = response['d']
    if 'data' in value:
        result = value['data']
        inst = sensors.getAllInstance()
        for element in inst:
            flowerID = newSQL.getFlowerpot(element.id)            
        if result['plantID'] == flowerID[0]:
            if result['order'] == "regar":
                GPIO.output(pinRegar, GPIO.HIGH)
                time.sleep(5)
                GPIO.output(pinRegar, GPIO.LOW)
                data = {"t": 7, "d": {"topic": "measures", "event": "message", "data":{"notification":"regado"}}}
                ws.send(json.dumps(data))
            if result['order'] == "iluminar":
                    GPIO.output(pinLuz, GPIO.HIGH)
                    GPIO.output(pinLuz, GPIO.LOW)
                    data = {"t": 7, "d": {"topic": "measures", "event": "message", "data":{"notification":"iluminado"}}}
                    ws.send(json.dumps(data))


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
        sensors.readThread()
        last = {}
        while True:
            lecturas = sensors.returnDataOnce()
            if (lecturas != last and lecturas != None):
                last = lecturas
                print(lecturas)
                data = {"t": 7, "d": {"topic": "measures", "event": "message", "data": lecturas}}
                ws.send(json.dumps(data))
            data = {"t": 7, "d": {"topic": "measures", "event": "message", "data":"ping-pong" }}
            ws.send(json.dumps(data))
            time.sleep(4)

    threading.Thread(target=run).start()



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
