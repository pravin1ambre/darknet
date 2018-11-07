from pymongo import MongoClient
from PIL import Image
import base64
import time
import glob, os
import sys, json
from publisher_subscriber import DataPublisher
import uuid
import socket
import shutil
from datetime import datetime


publisher = DataPublisher()
from detectobject import detect_object

def reduce_image_size(image_path,how_much):
    print("Got an image more than 400 kb")
    im = Image.open(image_path)
    width, height = im.size
    size = width / how_much, height / how_much
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(image_path)

def mongo_connection_with_collection():
    client = MongoClient('mongodb://localhost:27017')
    db = client['kkesani_3']
    col = db.timeseries_data
    col1 = db.config
    return col, col1


def fetch_image(image_str, count):
    fh = open("/home/EOG/kkesani/fetched_images/{}.jpg".format(count), "wb")
    fh.write(base64.b64decode(image_str))
    fh.close()
	
def resizeImage(img):    
    if os.path.getsize(img) > 50017:
        reduce_image_size(img, how_much=2)
    print("Now image Size: {}".format(os.path.getsize(img)))
    with open(img, "rb") as imageFile:
        img_str = base64.b64encode(imageFile.read())
    return img_str

def image_to_str(img, typ = None):
    with open(img, "rb") as imageFile:
        img_str = base64.b64encode(imageFile.read())
    return img_str

while True:
    #data_path = "C:\\Users\\kkesani\\Desktop\\images"
    data_path = "/home/images"
    files_with_path = glob.glob(data_path + "/*")
    print("Got {} files on  {}".format(len(files_with_path),data_path))
    col, col1 = mongo_connection_with_collection()
    prediction_image="{}/predictions.jpg".format(os.getcwd())
    for img in files_with_path:
        utc = int(time.time())
        #'/home/copy_images/'
        copy_path = "{}/{}".format('/home/copy_images/', str("".join(os.path.basename(img).split("_",2)[:2])))
        if not os.path.exists(copy_path):
            os.mkdir(copy_path)
        shutil.copy(img, copy_path)
        rename = str("_".join(os.path.basename(img).split("_",2)[:2]))+ str(int(time.time())) +'.jpg'
        os.rename(copy_path+"/"+ os.path.basename(img),copy_path+"/"+rename)

        data_dict = {}
        mac_address = "_".join(os.path.basename(img).split("_",3)[:3])
        mac_address_exists = col1.find_one({"mac_address": mac_address})
        print("Executing for {}".format(img))
        img_str = image_to_str(img)
        objects = ''
        predictions_image = image_to_str(prediction_image, typ="Prediction_image")
        if  mac_address_exists !=None and mac_address_exists['object_sync']:
            objects = detect_object(img)
            data_dict['objects'] = json.dumps(objects)
            data_dict['prediction_image'] = predictions_image

        if mac_address_exists == None:
            data = { 'mac_address': mac_address, 'object_sync': False,'tag'   : 'tag', 
                     'source_sync':True,  'thumbnail_sync': True , 'prediction_sync': False             }
            col1.insert_one(data)

        thumbnail_image = resizeImage(img)        
        data_dict['uuid']=  str(uuid.uuid1())
        data_dict['timestamp']= int(time.time())
        data_dict['mac_address']= mac_address
        data_dict['source']= img_str
        data_dict['thumbnail'] = thumbnail_image 
        col.insert_one(data_dict)       

        hostname = socket.gethostname()        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        publisher.send(json.dumps({
            'thumbnail' : thumbnail_image.decode(), 'uuid':data_dict['uuid'],'timestamp':data_dict['timestamp'],
            'mac_address': data_dict['mac_address'],'ip': s.getsockname()[0] , 'objects':json.dumps(objects) 
        }))
        s.close()
        time.sleep(1)
        os.remove(img)
    #wait for 1 minute
    time.sleep(2)