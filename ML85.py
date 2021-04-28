import RPi.GPIO as GPIO
import serial
import json
import threading


threads = []


class ML85:
    def __init__(self, id, name):
        self.id = id
        self.idName = name
        self.uvIntensity = None
        self.pinOut = 17
        GPIO.setup(self.pinOut, GPIO.OUT)
        self.type = "ML85"

    def read(self, jline):
                try:
                    if jLine["uvIntensity"]:
                        self.uvIntensity = jLine["uvIntensity"]
                        print(self.uvIntensity)
                except:
                    print("An exception occurred")


    def returnData(self):
        data = {'name': self.idName, 'data': [{"uvIntensity": self.uvIntensity}], 'type': self.type}
        return data
