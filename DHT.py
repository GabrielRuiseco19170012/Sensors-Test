from MySQL import *
from MongoDB import *
import Adafruit_DHT
import time
from datetime import datetime
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
newSQL = MySQL()
newMongo = MongoDB()


class DHT:
    def __init__(self, name):
        self.idName = name
        self.sensor = Adafruit_DHT.DHT11
        self.DHT11_pin = 4
        self.datos = (0, 0, "")
        self.temperature = 0
        self.humidity = 0
        self.type = 'DHT-11'
        self.pinOut = 17
        GPIO.setup(self.pinOut, GPIO.OUT)

    def read(self):
        self.humidity, self.temperature = Adafruit_DHT.read(self.sensor, self.DHT11_pin)
        if self.humidity is not None and self.temperature is not None:
            self.ahora = datetime.now()
            self.fecha = self.ahora.strftime("%Y-%m-%d %H:%M:%S")
            self.datos = (self.temperature, self.humidity, self.fecha)
            if self.temperature > 25:
                GPIO.output(self.pinOut, GPIO.HIGH)
            if self.temperature > 24:
                GPIO.output(self.pinOut, GPIO.LOW)
            time.sleep(1)

    def returnData(self):
        data = {'name': self.idName, 'data': [{"temperatude": self.temperature}, {"humidity": self.humidity}],
                'type': self.type}
        return data
