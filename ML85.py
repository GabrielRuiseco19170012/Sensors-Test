import RPi.GPIO as GPIO
import serial
import json
import threading
from datetime import datetime



threads = []


class ML85:
    def __init__(self, id, name):
        self.id = id
        self.idName = name
        self.uvIntensity = None
        self.pinOut = 17
        GPIO.setup(self.pinOut, GPIO.OUT)
        self.type = "ML85"

    def read(self, jLine):
                try:
                    if jLine["uvIntensity"]:
                        self.uvIntensity = jLine["uvIntensity"]
                        now = datetime.now()
                        data = {"IDSensor":self.id, "measurements": {"uvIntensity": self.uvIntensity}, "created_at": now}
                        return data
                except:
                    print("An exception occurred")


    def returnData(self):
        now = datetime.now()
#         timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        data = {"IDSensor":self.id, "measurements": {"uvIntensity": self.uvIntensity}, "created_at": now}
        return data
