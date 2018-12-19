from flask import Flask, render_template, Response
from flask_restful import Resource, Api
from flask_cors import CORS
from flask import jsonify
import glob
import os
import datetime
import time
# from flask_mysqldb import MySQL
import csv
from zipfile import ZipFile
import glob
import ast
import json
import base64
import shutil 
import pandas as pd
import re
app = Flask(__name__)
api = Api(app)
CORS(app)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
engine = create_engine('mysql://root:admin@localhost/io_dataload',echo=False)

#database configration with class

# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'Dad@12345'
# app.config['MYSQL_DB'] = 'io_dataload'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# mysql = MySQL(app)



class CsvRecords(Resource):
    def get(self):
        result = engine.execute('''select * from dataload limit 100''')
        return jsonify([(dict(row.items())) for row in result.fetchall()]) 


api.add_resource(CsvRecords, '/')

if __name__ == '__main__':
    app.run(port="5001", debug=True)

