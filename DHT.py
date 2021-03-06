from MySQL import *
from MongoDB import *
import Adafruit_DHT
import time
from datetime import datetime
import RPi.GPIO as GPIO
from datetime import datetime

GPIO.setmode(GPIO.BCM)
newSQL = MySQL()
newMongo = MongoDB()


class DHT:
    def __init__(self, id, name):
        self.id = id
        self.idName = name
        self.sensor = Adafruit_DHT.DHT11
        self.DHT11_pin = 4
        self.datos = (0, 0, "")
        self.temperature = 0
        self.humidity = 0
        self.type = 'DHT-11'

    def read(self):
        self.humidity, self.temperature = Adafruit_DHT.read(self.sensor, self.DHT11_pin)
        if self.humidity is not None and self.temperature is not None:
            self.ahora = datetime.now()
            self.fecha = self.ahora.strftime("%Y-%m-%d %H:%M:%S")
            self.datos = (self.temperature, self.humidity, self.fecha)
            time.sleep(1)

    def returnData(self):
        now = datetime.now()
#         timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        data = {"IDSensor":self.id, "measurements": {"temperature": self.temperature, "humidity": self.humidity}, "created_at": now}
        return data

