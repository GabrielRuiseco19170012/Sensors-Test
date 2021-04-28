from DHT import *
from HL69 import *
from ML85 import *
from DataList import DataList
from File import File
from MySQL import *
from MongoDB import *
from UData import USERID
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
        try:
            while True:
                for element in self.instancesList.getDataList():
                    if element.type == "DHT-11":
                        element.read()    
                    data = element.returnData()
                    if (data['data'] != {'temperature': None, 'humidity': None} and data['data'] != [{'grHumidity': None}] and data['data'] != [{'uvIntensity': None}]):
                        newMongo.insertDatosSensor(data)
        except KeyboardInterrupt:
            print("adios")
            sys.exit()

    def returnDataOnce(self):
        try:
            d=''
            for element in self.instancesList.getDataList():
                data = element.returnData()
                if (data['data'] != {'temperatude': None, 'humidity': None} and data['data'] != [{'grHumidity': None}] and data['data'] != [{'uvIntensity': 0}]):
                    d=data['data']
            return d
        except:
            raise
    
    
    def readThread(self):
        t = threading.Thread(name='Hilo', target=self.returnData)
        t.start()
        print('flagThread')
