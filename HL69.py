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
        self.humidity = 0
        self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        self.ser.flush()
        self.type = "HL-69"
        self.pinOut = 18
        GPIO.setup(self.pinOut, GPIO.OUT)

    def readData(self):
        while True:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').rstrip()
                try:
                    jLine = json.loads(line)
                    if jLine["grHumidity"]:
                        self.humidity = jLine["grHumidity"]
                        print(self.humidity)
                        if self.humidity < 10:
                            GPIO.output(self.pinOut, GPIO.HIGH)
                        if self.humidity > 95:
                            GPIO.output(self.pinOut, GPIO.LOW)
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
        data = {'name': self.idName, 'data': [{"grHumidity": self.humidity}], 'type': self.type}
        return data
