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
            dt = json.loads(result)
        if dt['plantID'] == flowerID[0]:
            if dt['order'] == "regar":
                GPIO.output(pinRegar, GPIO.HIGH)
                print(GPIO.input(pinRegar))
                time.sleep(5)
                GPIO.output(pinRegar, GPIO.LOW)
                print('end')
            if dt['order'] == "iluminar":
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
        sensors.readThread()
        ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        ser.flush()
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                print(line)
                try:
                    jLine = json.loads(line)
                    hl = sensors.getOneInstance("HL-69")
                    ml = sensors.getOneInstance("ML85")
                    if len(line) > 33:
                        if hl is not None:
                            hl.read(jline)
                        if ml is not None:
                            ml.read(jline)
                except:
                    print('fallo')

            d = sensors.returnDataOnce()
            data = {"t": 7, "d": {"topic": "measures", "event": "message", "data":d }}
            ws.send(json.dumps(data))
#             time.sleep(3)

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
