from flask import Flask, render_template, Response
from flask_restful import Resource, Api
from flask_cors import CORS
from flask import jsonify
import glob
import os
import datetime
import time
import csv
from zipfile import ZipFile
import glob
import ast
import json
import base64
import shutil 
import pandas as pd
import re
from sqlalchemy import *
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import platform

app = Flask(__name__)
api = Api(app)
CORS(app)

engine = create_engine('mysql://root:Dad@12345@localhost/io_dataload',echo=False)

meta = MetaData()

#create table in io_dataload ie dataload
maptable = Table('maptable', meta,
    Column('types', String, nullable=False),
    Column('name', String, nullable=False),
    Column('metrics', String, nullable=False)
)
maptable.create(engine,checkfirst=True) 

#path of the zip folder and backup in linux and windows machine
import_path = os.getcwd()+"/data_zip/"
export_path = os.getcwd()+"/zip_backup/"
map_file_path = os.getcwd()+'/54.txt'
if platform.system() == 'Windows':
    import_path = os.getcwd()+"\\data_zip\\"
    export_path = os.getcwd()+"\\zip_backup\\"
    map_file_path = os.getcwd()+'\\54.txt'

class StoreRecords(Resource):
    #extract zip file in data zip folder
    def getZip(self):
        zip_data = glob.glob( "{}{}".format(import_path,"*.zip"))
        if zip_data:
            for file_path in zip_data:
                zip_file = ZipFile(file_path)        
                zip_file.extractall(import_path)
                zip_file.close()

    #select all available csv files from data zip folder
    def insideFolder(self,import_path):        
        csv_files = []
        for dirpath, subdirs, files in os.walk(import_path):
            for file_name in files:
                if file_name.endswith(".csv"):
                    csv_files.append(os.path.join(dirpath, file_name))
        return self.sendToCsv(csv_files)

    #iterate all selected csv file and send to csvFile function
    def sendToCsv(self,csv_files): 
        for csv in csv_files:
            self.csvFile(csv)

    #map unique  key for maptable 
    def mapping_key(self):
        mapping_file = open(map_file_path,'r') 
        file_data = mapping_file.readlines()
        for data in file_data:
            table_data = data.split("\t\t")
            metrics = int(re.search(r'\d+', table_data[2]).group())
            result = engine.execute("select * from maptable where metrics='{}'".format(metrics)).fetchone()
            if  result == None:
                engine.execute('INSERT INTO maptable (types, name, metrics) VALUES (%s, %s, %s)', table_data[0], table_data[1], metrics)                

    #dataloading in database dataload table    
    def csvFile(self,csv_path): 
        print("---------------------------  -data is loading--  -------------",datetime.datetime.now())
        count = 0
        File = open(csv_path, encoding="utf8")
        csv_data = csv.reader(File)

        skiplist = []
        for row in list(csv_data):
            if  '#' in row[0]:
                skiplist.append(count)
            else:
                break
            count +=1
        df = pd.read_csv(csv_path ,skiprows = skiplist)
        
        times = df['Time'].apply(lambda x:x.split('.')[0])
        # unix_timestamp = df['Date'].apply(lambda x:time.mktime(datetime.datetime.strptime(x, "%Y/%m/%d").timetuple()))
        date_time = df['Date'].apply(lambda x: datetime.datetime.strptime(x, '%Y/%m/%d').strftime('%m-%d-%y')) +' '+ times
        unix_time = df['Date'].apply(lambda x: x) +' '+ times
        unix_timestamp = unix_time.apply(lambda x:time.mktime(datetime.datetime.strptime(x, "%Y/%m/%d %H:%M:%S").timetuple()))
        all_data = pd.DataFrame()
        for c_name in row[2:]:
            result = engine.execute("select metrics from maptable where name=%s",c_name).fetchone()[0]
            metrics = int(re.search(r'\d+', result).group())
            data = pd.DataFrame({'date':date_time,'value' : df[c_name],'metrics':metrics,'unix_timestamp':unix_timestamp, 
                                            'date_time':datetime.datetime.now()})
            all_data = all_data.append(data)           

        # data.to_sql('dataload', con=engine,if_exists='append',index=False)
        all_data.to_sql('dataload', con=engine,if_exists='append',index=False)

    #initial call of api and copy zip file in backup and after 
    #operation on file it delete zip and all extrated file
    def get(self):
        if os.listdir(import_path):
            for name in os.listdir(import_path):
                shutil.copy(import_path+name, export_path)
            self.getZip()
        else:
            print('------------no csv found------------------')
            return {'message': 'No csv found'}
        self.mapping_key()

        if os.listdir(import_path):
            self.insideFolder(import_path)
            print("----------------------------data upload successfully---------------",datetime.datetime.now())
            for name in os.listdir(import_path):
                if os.path.isdir(import_path+name):
                    shutil.rmtree(import_path+name)
                else:
                    os.remove(import_path+name)


if __name__ == '__main__':
    while True:
        obj = StoreRecords()
        obj.get()
        time.sleep(3)

