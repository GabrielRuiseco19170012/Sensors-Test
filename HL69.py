import RPi.GPIO as GPIO
import serial
import json
import threading
GPIO.setmode(GPIO.BCM)
from datetime import datetime


threads = []


class HL69:
    def __init__(self, id, name):
        self.id = id
        self.idName = name
        self.humidity = None
        self.type = "HL-69"
        self.pinOut = 18
        GPIO.setup(self.pinOut, GPIO.OUT)

    def read(self, jLine):
        try:
#             print(jLine)
            if jLine["grHumidity"]:
#                 print(jLine["grHumidity"])
                self.humidity = jLine["grHumidity"]
                print(self.humidity,"sisoyyo")
                now = datetime.now()
                data = {"IDSensor":self.id, "measurements": {"grHumidity": self.humidity}, "created_at": now}
                return data
        except Exception as e:
            print(e)

    def returnData(self):
        now = datetime.now()
#         timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        data = {"IDSensor":self.id, "measurements": {"grHumidity": self.humidity}, "created_at": now}
        return data
