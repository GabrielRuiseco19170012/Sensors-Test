import RPi.GPIO as GPIO
import serial
import json
import threading
GPIO.setmode(GPIO.BCM)

threads = []


class HL69:
    def __init__(self, id, name):
        self.id = id
        self.idName = name
        self.humidity = None
        self.type = "HL-69"
        self.pinOut = 18
        GPIO.setup(self.pinOut, GPIO.OUT)

    def read(self, jline):
        try:
            if jLine["grHumidity"]:
                self.humidity = jLine["grHumidity"]
                if self.humidity < 10:
                    GPIO.output(self.pinOut, GPIO.HIGH)
                if self.humidity > 95:
                    GPIO.output(self.pinOut, GPIO.LOW)
        except:
            print("Error")

    def returnData(self):
        data = {'name': self.idName, 'data': [{"grHumidity": self.humidity}], 'type': self.type}
        return data
