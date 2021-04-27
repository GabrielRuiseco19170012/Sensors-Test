import RPi.GPIO as GPIO
import serial
import json
import threading

threads = []


class ML85:
    def __init__(self, id, name):
        self.id = id
        self.idName = name
        self.uvIntensity = 0
        self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        self.ser.flush()
        self.pinOut = 17
        GPIO.setup(self.pinOut, GPIO.OUT)
        self.type = "ML85"

    def readData(self):
        while True:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').rstrip()
                try:
                    jLine = json.loads(line)
                    if jLine["uvIntensity"]:
                        self.uvIntensity = jLine["uvIntensity"]
                        print(self.uvIntensity)
                except:
                    print("An exception occurred")

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

    def returnData(self):
        data = {'name': self.idName, 'data': [{"uvIntensity": self.uvIntensity}], 'type': self.type}
        return data
