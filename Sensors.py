from DHT import *
from HL69 import *
from ML85 import *
from DataList import DataList
from File import File
from MySQL import *
from MongoDB import *
import sys

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
            if self.instancesList.getData(None, o['type']) is None:
                if o['name'][0:3] == 'DHT-11':
                    instance = DHT(o['name'])
                    self.instancesList.addData(instance)
                elif o['name'][0:3] == 'HL69':
                    instance = HL69(o['name'])
                    self.instancesList.addData(instance)
                elif o['name'][0:3] == 'ML85':
                    instance = ML85(o['name'])
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
                for element in sensorList:
                    element.read()
                    data = element.retunData()
                    if (data['data']==[None, None]):
                        newSQL.guardarDatos(data)
                        newMongo.insertDatosSensor(data)
                        file.append(data)
                        File.saveData(file)
                    else:
                        print('Error')
        except KeyboardInterrupt:
            print("adios")
            sys.exit()
