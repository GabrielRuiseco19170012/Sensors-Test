from mysql.connector.connection import MySQLConnection
from datetime import datetime


class MySQL:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "123456"
        self.database = "RaspberryData"

    def Conexion(self):
        try
            self.mydb = MySQLConnection(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except Exception as e
            self.mydb = MySQLConnection(
                host="localhost",
                user="root",
                password="123456",
                database="RaspberryData"
            )
        return "Conexion a MySQL exitosa"

    # DHT----------------------------------------------------------------
    def guardarDatos(self, data):
        self.sql = "insert into Sensors (IDName, Data, Type) values (%s, %s, %s)"
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute(self.sql, (data['name'], str(data['data']), data['type']))
        self.mydb.commit()

    def getSensors(self):
        self.sql = "select * from sensors_inst"
        try:
            self.mycursor = self.mydb.cursor()
            self.mycursor.execute(self.sql)
            data = self.mycursor.fetchall()
            return data
        except Exception as e:
            raise e
