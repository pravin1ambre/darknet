from flask import Flask, render_template, Response
from flask_restful import Resource, Api
from flask_cors import CORS
from flask import jsonify
import glob
import os

import ast
import json
import base64
from bson import json_util

app = Flask(__name__)
api = Api(app)
CORS(app)
import PyMySQL


class GetRecords(Resource):
    def get(self):
        from zipfile import ZipFile
        zf = ZipFile('HP444 Cobalt 32 State 707H TDI-712-MLA01-012 - output data.csv.zip', 'r')
        zf.extractall('/home/pravin/confidential/')
        zf.close()
        import datetime, os

        mapping_file = open('54.txt','r') 
        data = mapping_file.readlines()
        keys = []
        for da in data:
            ta = da.split("\t\t")
            keys.append(ta[2].split('\t\r\n')[0])

        import csv
        import MySQLdb

        mydb = PyMySQL.connect(host='localhost',
            user='root',
            passwd='admin',
            db='test')
        cursor = mydb.cursor()
        count = 0
        csv_data = csv.reader(file('HP444 Cobalt 32 State 707H TDI-712-MLA01-012 - output data.csv'))
        for row in csv_data:
            if not '#' in row[0]:
                if count:
                    cnt = 0
                    for r in row[2:]:
                        try: 
                            key = keys[cnt]
                        except:
                            key = None  
                        cnt +=1   
                        cursor.execute('INSERT INTO csvdata(Date, Time,matrics,value,timestamp) VALUES("{}", "{}", "{}","{}","{}")'.format(row[0],row[1],key,r,datetime.datetime.now()))
                count += 1
                
        #close the connection to the database.
        mydb.commit()
        cursor.close()



api.add_resource(GetRecords, '/store')

if __name__ == '__main__':
    app.run(port="5001", debug=True)

