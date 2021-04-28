import pymongo


class MongoDB:
    def __init__(self):
        pass

    def mongoConexion(self):
        self.Mongo_URI = "mongodb+srv://14777:14777@cluster0.pltuv.mongodb.net/adonis?retryWrites=true&w=majority"
        # self.Mongo_URI="mongodb://"+self.Mongo_Host+":"+self.Mongo_Port+"/"
        try:
            # self.cliente = pymongo.MongoClient(self.Mongo_URI)
            self.cliente = pymongo.MongoClient(self.Mongo_URI)
            self.cliente.server_info()
            return "Conexion a MongoDB Exitosa"
        except pymongo.errors.ConnectionFailure as errorConexion:
            self.cliente = pymongo.MongoClient('localhost', 27017)
            self.cliente.server_info()

    def insertDatosSensor(self, data):
        try:
            self.mydb = self.cliente['adonis']
            self.tabla = self.mydb['measurements']
            self.datosIns = self.tabla.insert_one(data)
            return "Datos del Sensor insertados a MongoDB"
        except:
            return "No se insertado"
