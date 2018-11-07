from flask import Flask, render_template, Response
from flask_restful import Resource, Api
from flask_cors import CORS
from flask import jsonify
import glob
import os

from pymongo import MongoClient
import ast

app = Flask(__name__)
api = Api(app)
CORS(app)
#mongo db
#app.config['MONGO_DBNAME'] = 'kkesani_3'
#app.config['MONGO_URI'] = 'mongodb://localhost:27017/kkesani_3'
#mongo = PyMongo(app)

def mongo_connection_with_collection():
    client = MongoClient('mongodb://localhost:27017')
    db = client['kkesani_3']
    col = db.timeseries_image
    col1 = db.config
    return col, col1

class GetRecords(Resource):
    def get(self):
        col, col1 = mongo_connection_with_collection()
        #col = mongo.db.image
        data = col.find()
        records = []
        for i in data:
            info  = {
                'objects': ast.literal_eval(i['objects']) if 'objects' in i else '' , 
                'name':i['timestamp_thumbnail_image'],
                'timestamp':  i['timestamp'],
                'image':  i['image'].decode("utf-8"),
                'prediction_image': i['prediction_image'].decode("utf-8") if 'prediction_image' in i else '' ,
                'thumbnail': i['thumbnail'].decode("utf-8"),
            }
            records.append(info)
        return  records[::-1]

class SearchRecords(Resource):
    def get(self,name):
        col, col1 = mongo_connection_with_collection()
        data = col.find({"name":{"$regex": u"{}".format(name), "$options": "-i"}})
        records = []
        for i in data:        
            sata  = {'objects': ast.literal_eval(i['objects']),
                'name':i['name'],
                'timestamp':  i['timestamp'],
                'image': i['image'].decode("utf-8"),
                'prediction_image': i['prediction_image'].decode("utf-8"),
                'thumbnail': i['thumbnail'].decode("utf-8"),
            }
            records.append(sata)
			
        return  records[::-1]

class LatestImages(Resource):
    def get(self):
        imagelist = glob.glob("/home/pravin/project/darknet/darknet/images/*")
        list = [os.path.basename(i) for i in imagelist]
        return list      
        
class Algoritham(Resource):
    def get(self,name):
        col, col1 = mongo_connection_with_collection()
        data = { 'mac_address': name, 'action': 1, 'tag' : 'tag' }
        col1.insert_one(data)
        return True

class Database(Resource):
    def get(self,name):
        col, col1 = mongo_connection_with_collection()
        data = { 'mac_address': name, 'action': 0,'tag'   : 'tag' }
        col1.insert_one(data)
        return True
    

api.add_resource(GetRecords, '/images')
api.add_resource(SearchRecords, '/search/<string:name>')
api.add_resource(Algoritham, '/algorithm/<string:name>')
api.add_resource(Database, '/database/<string:name>')
api.add_resource(LatestImages, '/latest')

if __name__ == '__main__':
    app.run(port="5001", debug=True)

