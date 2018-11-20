import ast
import base64
import json
import os
import requests
from bson import json_util
from pymongo import MongoClient
from detectobject import detect_object
from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource
from publisher_subscriber import DataPublisher
publisher = DataPublisher()
import socket
from logger import exception

app = Flask(__name__)
api = Api(app)
CORS(app)
MONGO_HOST = 'localhost'
MONGO_PORT = '27017'
MONGO_DB = 'kkesani_3'
db = MongoClient('mongodb://{}:{}'.format(MONGO_HOST, MONGO_PORT))[MONGO_DB]

class GetRecords(Resource):
    @exception
    def get(self, id):
        data = db.timeseries_data.find().sort([("_id", -1)]).skip(int(id)).limit(10)
        count =10
        page_count = 0
        for i in db.timeseries_data.find().skip(count).limit(10):
            if len(list(i)):
                page_count = page_count +1
                count = count+10
                page_count-2
            else:
                break  
        if page_count == 0:
            page_count = 1
        all_counts = db.timeseries_data.find().count()
        records = []
        for i in data:
            try:
                objects = ast.literal_eval(i.get('objects'))
            except:
                objects = ''
            info  = {
                'objects': objects, 
                'mac_address':i['mac_address'],
                'timestamp':  i['timestamp'],
                'source':  i['source'].decode("utf-8"),
                'prediction_image': i['prediction_image'].decode("utf-8") if 'prediction_image' in i else '' ,
                'thumbnail': i['thumbnail'].decode("utf-8"),
            }
            records.append(info)
        return  {'data' : records, 'count' : all_counts,'pages':page_count, 'current_page' : 1 if int(id) == 0 else (int(id)/10)+1}

class SearchRecords(Resource):
    @exception
    def get(self,name):
        data = db.timeseries_data.find({"timestamp":{"$regex": u"{}".format(str(name))}})
        records = []
        for i in data:
            try:
                objects = ast.literal_eval(i.get('objects'))
            except:
                objects = ''        
            info  = {
                'objects': objects , 
                'mac_address':i['mac_address'],
                'timestamp':  i['timestamp'],
                'source':  i['source'].decode("utf-8"),
                'prediction_image': i['prediction_image'].decode("utf-8") if 'prediction_image' in i else '' ,
                'thumbnail': i['thumbnail'].decode("utf-8"),
            }
            records.append(info)
			
        return  records[::-1]



class Configuration(Resource):
    @exception
    def get(self, id):
        data =list(db.config.find().skip(int(id)).limit(10))
        count =10
        page_count = 0
        for i in db.config.find().skip(count).limit(10):
            if len(list(i)):
                page_count = page_count +1
                count = count+10
                page_count-2
            else:
                break
        if page_count == 0:
            page_count = 1

        return {'data':json.loads(json.dumps(data, default=json_util.default)),'count' : db.config.find().count(), 'pages':page_count, 'current_page' : 1 if int(id) == 0 else (int(id)/10)+1}


class ObjectDetection(Resource):
    @exception
    def get(self,name):
        data = db.config.find_one({"mac_address": name})
        if not data['object_sync']:
            db.config.update_one(
                {"mac_address": name},
                {
                    "$set": {
                        "object_sync":  not data['object_sync'] ,
                        "prediction_sync":  not data['prediction_sync'] ,                    
                    }
                }
            )
            data = db.config.find_one({"mac_address": name})

            timeseries_data = db.timeseries_data.find_one({"mac_address": name})
            fh = open("{}/predictions.jpg".format(os.getcwd()), "wb")        
            fh.write(base64.b64decode(timeseries_data['source'])) 
            fh.close()
            object_data = json.dumps(detect_object(os.getcwd()+'/predictions.jpg'))
            with open(os.getcwd()+'/predictions.jpg',"rb") as img:
                img = base64.b64encode(img.read())
            timeseries_data = db.timeseries_data.find_one({"mac_address": name})
            if data['object_sync']:
                db.timeseries_data.update_one(
                    {"mac_address": name},
                    {
                        "$set": {
                            "objects": object_data,
                            "prediction_image":  img ,                    
                        }
                    }
                )
            info = db.timeseries_data.find_one({"mac_address": name})
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
api.add_resource(Configuration, '/configuration/<int:id>')
api.add_resource(ObjectDetection, '/detect-object/<string:name>')

if __name__ == '__main__':
    #app.run(host='10.11.128.61',port="5001", debug=True)
    app.run(port="5001", debug=True)
