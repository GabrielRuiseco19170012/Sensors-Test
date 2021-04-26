import RPi.GPIO as GPIO
import time
from datetime import datetime
from MySQL import *
from MongoDB import *
import threading
import time

threads = []


class HCR:
    def __init__(self, name, trigger, echo):
        self.idName = name
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.GPIO_TRIGGER = trigger
        self.GPIO_ECHO = echo
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)
        self.StartTime = 0
        self.StopTime = 0
        self.TimeElapsed = 0
        self.distance = 0
        self.type = 'HCR'

    def readData(self):
        GPIO.output(self.GPIO_TRIGGER, True)

        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)

        self.StartTime = time.time()
        self.StopTime = time.time()

        while GPIO.input(self.GPIO_ECHO) == 0:
            self.StartTime = time.time()

        while GPIO.input(self.GPIO_ECHO) == 1:
            self.StopTime = time.time()

        self.TimeElapsed = self.StopTime - self.StartTime
        self.distance = (self.TimeElapsed * 34300) / 2

    def returnData(self):
        data = {'name': self.idName, 'data': [self.distance], 'type': self.type}
        return data

    def read(self):
        name = self.idName
        status = False
        t = threading.Thread(name='Hilo' + self.idName, target=self.readData)
        for x in threads:
            if x == name:
                status = status
            else:
                status = True
        if status == True:
            t.start()
        else:
            return
