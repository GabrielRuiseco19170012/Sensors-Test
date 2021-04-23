import RPi.GPIO as GPIO
import time
from MySQL import *
from MongoDB import *
from datetime import datetime

newSQL = MySQL()
newMongo = MongoDB()


class PIR:
    def __init__(self, name, pin):
        self.idName = name
        GPIO.setmode(GPIO.BCM)
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN, GPIO.PUD_DOWN)
        self.estado_anterior = False
        self.estado_actual = False
        self.nuevo_estado = ""
        self.datos = ("", "")
        self.type = 'PIR'
        newSQL.Conexion()
        newMongo.mongoConexion()

    def read(self):
        self.estado_previo = self.estado_actual
        self.estado_actual = GPIO.input(self.pin)
        if self.estado_actual != self.estado_previo:
            self.nuevo_estado = "DETECTADO" if self.estado_actual else "NON"
            self.ahora = datetime.now()
            self.fecha = self.ahora.strftime("%Y-%m-%d %H:%M:%S")
            self.datos = (self.nuevo_estado, self.fecha)
            time.sleep(1)

    def returnData(self):
        data = {'name': self.idName, 'data': [self.datos], 'type': self.type}
        return data
