from flask import Flask, render_template, Response, jsonify
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
from flask_marshmallow import Marshmallow


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost/io_dataload'

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Dataload(db.Model):
    date = db.Column(db.Text())
    value = db.Column(db.Float())  
    metrics = db.Column(db.BigInteger())
    unix_timestamp = db.Column('unix_timestamp', db.Float, primary_key = True)
    date_time = db.Column(db.DateTime())

    def __init__(self, date, value, metrics, unix_timestamp, date_time):
        self.date = date
        self.value = value
        self.metrics = metrics
        self.unix_timestamp = unix_timestamp
        self.date_time = date_time

# db.create_all()

class DataloadSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('date', 'value','metrics','unix_timestamp','date_time')

dataload_schema = DataloadSchema()
dataload_schemas = DataloadSchema(many=True)


class CsvRecords(Resource):
    def get(self,page=1,):
        PER_PAGE = 10
        try:
            dataload = Dataload.query.order_by(
                Dataload.date_time.desc()
            ).paginate(page, per_page=PER_PAGE)
        except OperationalError:
            flash("No Data in the database.")
            dataload = None
        result = dataload_schemas.dump(dataload.items)
        return jsonify(result.data)


api.add_resource(CsvRecords, '/page/<int:page>')

if __name__ == '__main__':
    app.run(port="5001", debug=True)