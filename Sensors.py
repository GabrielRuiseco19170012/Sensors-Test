from DHT import *
from HL69 import *
from ML85 import *
from DataList import DataList
from File import File
from MySQL import *
from MongoDB import *
import sys

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
        self.id = 1
        self.instancesList = DataList()
        self.createInstances()

    def createInstances(self):
        print(sensorList)
        for o in sensorList:
                if o[3] == 'DHT-11':
                    instance = DHT(o[0], o[1])
                    self.instancesList.addData(instance)
                elif o[3] == 'HL-69':
                    instance = HL69(o[0], o[1])
                    self.instancesList.addData(instance)
                elif o[3] == 'ML85':
                    instance = ML85(o[0], o[1])
                    self.instancesList.addData(instance)
                else:
                    print('error al generar instancia')

    def getOneInstance(self, name):
        return self.instancesList.getData(name)

    def getAllInstance(self):
        return self.instancesList.getDataList()

    def returnData(self):
        try:
            while True:
                for element in self.instancesList.getDataList():
                    element.read()
                    data = element.returnData()
                    if (data['data'] != {'temperatude': None, 'humidity': None} and data['data'] != [{'grHumidity': 0}] and data['data'] != [{'uvIntensity': 0}]):
                        newMongo.insertDatosSensor(data)
                    else:
                        #print('Error')
                        return
        except KeyboardInterrupt:
            print("adios")
            sys.exit()

    def readThread(self):
        t = threading.Thread(name='Hilo', target=self.returnData)
        t.start()
