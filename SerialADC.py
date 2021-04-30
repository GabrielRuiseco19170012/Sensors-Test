import serial
import threading
import json

class SerialADC:

    @staticmethod
    def serialRead(ser,element):
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                if len(line) > 33:
                    jLine = json.loads(line)
                    data= element.read(jLine)
        except Exception as e:
            raise e
                
    @staticmethod
    def readSerial():
        t = threading.Thread(name='Hilo', target=SerialADC.serialRead)
        t.start()