from flask import Flask, render_template, Response
from flask_restful import Resource, Api
from flask_cors import CORS
from flask import jsonify
import glob
import os
from flask_mysqldb import MySQL

import ast
import json
import base64
from bson import json_util

app = Flask(__name__)
api = Api(app)
CORS(app)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'test'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/')
def users():
    cur = mysql.connection.cursor()
    cur.execute('''select * from csvdata''')
    rv = cur.fetchall()
    return str(rv)


class GetRecords(Resource):
    def get(self):
        from zipfile import ZipFile
        zf = ZipFile('/home/pravin/project/darknet/rest_flask/HP444.zip')
        zf.extractall('/home/pravin/project/darknet/rest_flask/')
        zf.close()
        import datetime, os

        cur = mysql.connection.cursor()


        mapping_file = open('54.txt','r') 
        data = mapping_file.readlines()
        keys = []
        for da in data:
            ta = da.split("\t\t")
            keys.append(ta[2].split('\t\r\n')[0])

        import csv
        count = 0
        File = open('/home/pravin/project/darknet/rest_flask/HP444.csv')
        csv_data = csv.reader(File)
        # csv_data = csv.reader(file('/home/pravin/project/darknet/rest_flask/HP444.csv'))
        for row in list(csv_data):
            if not '#' in row[0]:
                if count:
                    cnt = 0
                    for r in row[2:]:
                        print(r)
                        try: 
                            key = keys[cnt]
                        except:
                            key = None  
                        cnt +=1   
                        cur.execute('INSERT INTO csvdata(Date, Time,matrics,value,timestamp) VALUES("{}", "{}", "{}","{}","{}")'.format(row[0],row[1],key,r,datetime.datetime.now()))
                count += 1
                
        #close the connection to the database.
        mysql.connection.commit()
        rv = cur.fetchall()
        return str(rv)


api.add_resource(GetRecords, '/store')

if __name__ == '__main__':
    app.run(port="5001", debug=True)

