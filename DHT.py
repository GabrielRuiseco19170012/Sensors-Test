from MySQL import *
from MongoDB import *
import Adafruit_DHT
import time
from datetime import datetime

newSQL = MySQL()
newMongo = MongoDB()


class DHT:
    def __init__(self, name, DHTPIN):
        self.idName = name
        self.sensor = Adafruit_DHT.DHT11
        self.DHT11_pin = DHTPIN
        self.datos = (0, 0, "")
        self.temperature = 0
        self.humidity = 0
        self.type = 'DHT'
        newSQL.Conexion()
        newMongo.mongoConexion()

    def read(self):
        self.humidity, self.temperature = Adafruit_DHT.read(self.sensor, self.DHT11_pin)
        if self.humidity is not None and self.temperature is not None:
            self.ahora = datetime.now()
            self.fecha = self.ahora.strftime("%Y-%m-%d %H:%M:%S")
            self.datos = (self.temperature, self.humidity, self.fecha)
            time.sleep(1)

    def returnData(self):
        data = {'name': self.idName, 'data': [self.temperature, self.humidity], 'type': self.type}
        return data
