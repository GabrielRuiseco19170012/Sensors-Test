import pymysql
from datetime import datetime


class MySQL:
    def __init__(self):
        self.host = "us-cdbr-east-03.cleardb.com"
        self.user = "b12f752de2a06b"
        self.password = "cb29f57b"
        self.database = "heroku_29f382185e3d44a"

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

    def getUserID(self, data):
        self.sql1 = "select user_id from gardens where id = (select garden from flowerpots where id = (select IDFlowerpot from flowerpot_sensors where IDSensor = %s))"
        try:
            self.mycursor = self.mydb.cursor()
            self.mycursor.execute(self.sql1, data)
            res = self.mycursor.fetchone()
            return res
        except Exception as e:
            raise e

    def getFlowerpot(self, data):
        self.sql1 = "select IDFlowerpot from flowerpot_sensors where IDSensor = %s"
        try:
            self.mycursor = self.mydb.cursor()
            self.mycursor.execute(self.sql1, data)
            res = self.mycursor.fetchone()
            return res
        except Exception as e:
            raise e