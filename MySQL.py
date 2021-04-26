import pymysql
from datetime import datetime


class MySQL:
    def __init__(self):
        self.host = "localhost"
        self.user = "user"
        self.password = ""
        self.database = "adonis"

    def Conexion(self):
        try:
            self.mydb = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except Exception as e:
            self.mydb = pymysql.connect(
                host="localhost",
                user="user",
                password="",
                database="adonis"
            )
        return "Conexion a MySQL exitosa"

    # DHT----------------------------------------------------------------
    def guardarDatos(self, data):
        self.sql = "insert into Sensors (IDName, Data, Type) values (%s, %s, %s)"
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute(self.sql, (data['name'], str(data['data']), data['type']))
        self.mydb.commit()

    def getSensors(self):
        self.sql = "select * from sensors"
        try:
            self.mycursor = self.mydb.cursor()
            self.mycursor.execute(self.sql)
            data = self.mycursor.fetchall()
            return data
        except Exception as e:
            raise e
