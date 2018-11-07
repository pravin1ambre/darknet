from flask import Flask, render_template, Response
from flask_restful import Resource, Api
from flask_cors import CORS
from flask import jsonify
import glob
import os

from pymongo import MongoClient
import ast
import json
import base64
from bson import json_util
from detectobject import detect_object
from publisher_subscriber import DataPublisher
publisher = DataPublisher()
import socket


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
    col = db.timeseries_data
    col1 = db.config
    return col, col1

col, col1 = mongo_connection_with_collection()

class GetRecords(Resource):
    def get(self, id):
        col, col1 = mongo_connection_with_collection()
        #col = mongo.db.image
        data = col.find().skip(int(id)).limit(10)
        records = []
        for i in data:
            info  = {
                'objects': ast.literal_eval(i['objects']) if 'objects' in i else '' , 
                'mac_address':i['mac_address'],
                'timestamp':  i['timestamp'],
                'source':  i['source'].decode("utf-8"),
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
            info  = {
                'objects': ast.literal_eval(i['objects']) if 'objects' in i else '' , 
                'mac_address':i['mac_address'],
                'timestamp':  i['timestamp'],
                'source':  i['source'].decode("utf-8"),
                'prediction_image': i['prediction_image'].decode("utf-8") if 'prediction_image' in i else '' ,
                'thumbnail': i['thumbnail'].decode("utf-8"),
            }
            records.append(info)
			
        return  records[::-1]



class Configuration(Resource):
    def get(self):
        data =list(col1.find())
        return json.loads(json.dumps(data, default=json_util.default))



class SearchConfiguration(Resource):
    def get(self, name):
        print('Hiii')


class ObjectDetection(Resource):
    def get(self,name):
        data = col1.find_one({"mac_address": name})
        if not data['object_sync']:
            col1.update_one(
                {"mac_address": name},
                {
                    "$set": {
                        "object_sync":  not data['object_sync'] ,
                        "prediction_sync":  not data['prediction_sync'] ,                    
                    }
                }
            )
            data = col1.find_one({"mac_address": name})

            timeseries_data = col.find_one({"mac_address": name})
            fh = open("{}/predictions.jpg".format(os.getcwd()), "wb")        
            fh.write(base64.b64decode(timeseries_data['source'])) 
            fh.close()
            object_data = json.dumps(detect_object(os.getcwd()+'/predictions.jpg'))
            with open(os.getcwd()+'/predictions.jpg',"rb") as img:
                img = base64.b64encode(img.read())
            timeseries_data = col.find_one({"mac_address": name})
            if data['object_sync']:
                col.update_one(
                    {"mac_address": name},
                    {
                        "$set": {
                            "objects": object_data,
                            "prediction_image":  img ,                    
                        }
                    }
                )
            info = col.find_one({"mac_address": name})
            hostname = socket.gethostname()        
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))        
            publisher.send(json.dumps({
                'thumbnail' : info['thumbnail'].decode(), 'uuid' : info['uuid'], 'objects': object_data, 'timestamp':info['timestamp'],
                'mac_address': info['mac_address'],'ip': s.getsockname()[0]
            }))
            s.close()
            return json.loads(json.dumps(data, default=json_util.default))



api.add_resource(GetRecords, '/images/<int:id>')
api.add_resource(SearchRecords, '/search/<string:name>')
api.add_resource(Configuration, '/configuration')
api.add_resource(ObjectDetection, '/detect-object/<string:name>')
api.add_resource(SearchConfiguration, '/configuration/<string:name>')

if __name__ == '__main__':
    app.run(host='10.11.128.61',port="5001", debug=True)
    #app.run(port="5001", debug=True)