from DHT import *
from HL69 import *
from ML85 import *
from DataList import DataList
from File import File
from MySQL import *
from MongoDB import *
from UData import USERID
import threading
import sys
import serial
import json

threads = []

try:
    file = File.readData()
except Exception as e:
    file = []

newSQL = MySQL()
newMongo = MongoDB()
newSQL.Conexion()
newMongo.mongoConexion()
sensorList = newSQL.getSensors()


class Sensors:

    def __init__(self):
        self.instancesList = DataList()
        self.createInstances()

    def createInstances(self):
        for o in sensorList:
            try:
                uid = newSQL.getUserID(o[0])
                if uid[0] == USERID:
                    if o[2] == 'DHT-11':
                        instance = DHT(o[0], o[1])
                        self.instancesList.addData(instance)
                    elif o[2] == 'HL-69':
                        instance = HL69(o[0], o[1])
                        self.instancesList.addData(instance)
                    elif o[2] == 'ML85':
                        instance = ML85(o[0], o[1])
                        self.instancesList.addData(instance)
                    else:
                        print('error al generar instancia')
            except:
                print('exeption')

    def getOneInstance(self, typ):
        return self.instancesList.getData(None,typ)

    def getAllInstance(self):
        return self.instancesList.getDataList()

    def returnData(self):
        jLine={}
        ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        ser.flush()
        try:
            while True:
                for element in self.instancesList.getDataList():
                    if element.type == "DHT-11":
                        element.read()
                        data = element.returnData()
                    try:
                        if element.type == "HL-69" or element.type == "ML85":
                            if ser.in_waiting > 0:
                                line = ser.readline().decode('utf-8').rstrip()
                                if len(line) > 33:
                                    jLine = json.loads(line)
                                    data= element.read(jLine)
                    except Exception as e:
                        raise e
                    if data:
                        if (data['measurements'] != {'temperature': None, 'humidity': None} and data['measurements'] != {'grHumidity': None} and data['measurements'] != {'uvIntensity': None}):
                            newMongo.insertDatosSensor(data)
                            actualData = data;
        except KeyboardInterrupt:
            print("adios")
            sys.exit()

    def returnDataOnce(self):
        try:
            d=''
            for element in self.instancesList.getDataList():
                if element.type == "DHT-11":
                    data = element.returnData()
                    if (data['measurements'] != {'temperature': None, 'humidity': None} and data['measurements'] != {'grHumidity': None} and data['measurements'] != {'uvIntensity': 0}):
                        d=data['measurements']
                        return d
        except:
            raise
    
    
    def readThread(self):
        t = threading.Thread(name='Hilo', target=self.returnData)
        t.start()
        print('flagThread')
