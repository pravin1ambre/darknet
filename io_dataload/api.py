from flask import Flask, render_template, Response
from flask_restful import Resource, Api
from flask_cors import CORS
from flask import jsonify
import glob
import os
import datetime
import time
from flask_mysqldb import MySQL
import csv
from zipfile import ZipFile
import glob
import ast
import json
import base64
import shutil 
app = Flask(__name__)
api = Api(app)
CORS(app)

#database configration with class
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'io_dataload'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


class CsvRecords(Resource):
    def get(self):
        cur = mysql.connection.cursor()
        cur.execute('''select * from dataload''')
        rv = cur.fetchall()
        return str(rv) 

class StoreRecords(Resource):
    def getZip(self):
        zip_data = glob.glob(os.getcwd()+"/data_zip/*.zip")
        if zip_data:
            for i in zip_data:
                print (os.getcwd()+"/zip_backup")
                shutil.copy(i, os.getcwd()+"/zip_backup")
                zf = ZipFile(i)        
                zf.extractall(os.getcwd()+"/data_zip/")
                zf.close()

    def insideFolder(self,dir_path):
        csv_files= glob.glob(dir_path + "/*.csv")
        condition = True
        while condition:
            condition = False
            for i in  os.listdir(dir_path):
                if  os.path.isdir(dir_path+"/"+i):
                    csv_files.extend( glob.glob("{}/{}/{}".format(dir_path,i,"*.csv")))
                    dir_path = "{}/{}".format(dir_path, i)
                    for j in  os.listdir(dir_path):
                        if  os.path.isdir(dir_path+"/"+j):
                            condition = True

        self.sendToCsv(csv_files)

    def sendToCsv(self,csv_files):
        for csv in csv_files:
            self.csvFile(csv)

    def mapping_key(self):
        mapping_file = open(os.getcwd()+'/54.txt','r') 
        data = mapping_file.readlines()
        keys = []
        for da in data:
            ta = da.split("\t\t")
            keys.append(ta[2].split('\t\r\n')[0])
        return keys

    
    def csvFile(self,csv_path):
        cur = mysql.connection.cursor()
        keys = self.mapping_key()
        count = 0
        File = open(csv_path)
        csv_data = csv.reader(File)
        for row in list(csv_data):
            if not '#' in row[0]:
                date = row[0].split("/")
                try : 
                    date = date[1]+"-"+date[2] + "-"+ date[0] + " " +row[1]
                except:
                    date = date
                if count:
                    cnt = 0
                    for r in row[2:]:
                        print(r)
                        try: 
                            key = keys[cnt]
                        except:
                            key = None  
                        cnt +=1   
                        cur.execute('INSERT INTO dataload(date,unix_timestamp,metrics,value,date_time) VALUES("{}", "{}", "{}","{}","{}")'.format(date,
                            time.mktime(datetime.datetime.strptime(row[0], "%Y/%m/%d").timetuple()),
                            key,r,datetime.datetime.now()))
                        break
                count += 1                
        mysql.connection.commit()
        return cur.fetchall()

    def get(self):
        if os.listdir(os.getcwd()+"/data_zip"):
            self.getZip()
        else:
            return {'message': 'No csv found'}
        data = ''
        if os.listdir(os.getcwd()+"/data_zip"):
            folder = glob.glob(os.getcwd()+"/data_zip/*")
            
            for i in folder:
                if os.path.isdir(i):
                    data = self.insideFolder(i)
                    break #single csv file
                elif i.endswith('.csv'):
                    data = self.csvFile(i)

            shutil.rmtree(os.getcwd()+"/data_zip")
            os.makedirs(os.getcwd()+"/data_zip")
        return str(data)


api.add_resource(CsvRecords, '/')
api.add_resource(StoreRecords, '/store')

if __name__ == '__main__':
    app.run(port="5001", debug=True)

