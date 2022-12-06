from flask import jsonify
import pymysql
import json

class DataBase:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='flaskImageUpload'
        )
        print("Connexión establecida")
        self.cursor = self.connection.cursor()

    def uploadImage(self, path, description = "none" ):
        sql = 'INSERT INTO uploads(path,description) values("{}","{}")'.format(path, description)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            raise