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
from PIL import ImageFile
from logger import exception
ImageFile.LOAD_TRUNCATED_IMAGES = True


publisher = DataPublisher()
from detectobject import detect_object

MONGO_HOST = 'localhost'
MONGO_PORT = '27017'
MONGO_DB = 'kkesani_3'
IMAGE_PATH = '/home/pravin/project/darknet/darknet/images/'
DATASCIENCE_IMAGE_PATH = '/home/pravin/data_science_images/'
IMG_SLEEP_TIME = 1
PROCESS_SLEEP_TIME = 2
MAX_IMG_SIZE = 50017
RECORDS_EXPIRY_SECONDS = 60
db = MongoClient('mongodb://{}:{}'.format(MONGO_HOST, MONGO_PORT))[MONGO_DB]
db.timeseries_data.ensure_index("creationTime",
                       expireAfterSeconds=RECORDS_EXPIRY_SECONDS)
db.config.ensure_index("creationTime",
                       expireAfterSeconds=RECORDS_EXPIRY_SECONDS)


@exception
def reduce_image_size(image_path,how_much):
    print("Got an image more than 400 kb")
    im = Image.open(image_path)
    dim =(500,500)
    newimg = im.resize(dim)
    newimg.save(image_path)

@exception	
def resizeImage(img):    
    if os.path.getsize(img) > MAX_IMG_SIZE:
        reduce_image_size(img, how_much=2)
    print("Now image Size: {}".format(os.path.getsize(img)))
    with open(img, "rb") as imageFile:
        img_str = base64.b64encode(imageFile.read())
    return img_str

@exception
def image_to_str(img, typ = None):
    with open(img, "rb") as imageFile:
        img_str = base64.b64encode(imageFile.read())
    return img_str

while True:
    #data_path = "C:\\Users\\kkesani\\Desktop\\images"
    data_path = "{}/images/".format(os.getcwd())
    files_with_path = glob.glob(data_path + "/*")
    print("Got {} files on  {}".format(len(files_with_path),data_path))
    prediction_image="{}/predictions.jpg".format(os.getcwd())
    for img in files_with_path:
        utc = int(time.time())
        #'/home/copy_images/'
        copy_path = "{}/{}".format('/home/pravin/', str("".join(os.path.basename(img).split("_",2)[:2])))
        if not os.path.exists(copy_path):
            os.mkdir(copy_path)
        shutil.copy(img, copy_path)
        rename = str("_".join(os.path.basename(img).split("_",2)[:2]))+ str(int(time.time())) +'.jpg'
        os.rename(copy_path+"/"+ os.path.basename(img),copy_path+"/"+rename)

        data_dict = {}
        mac_address = "_".join(os.path.basename(img).split("_",3)[:3])
        mac_address_exists = db.config.find_one({"mac_address": mac_address})
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
            db.config.insert_one(data)

        thumbnail_image = resizeImage(img)        
        data_dict['uuid']=  str(uuid.uuid1())
        data_dict['timestamp']= int(time.time())
        data_dict['mac_address']= mac_address
        data_dict['source']= img_str
        data_dict['thumbnail'] = thumbnail_image 
        data_dict["creationTime"] = datetime.now(),
        db.timeseries_data.insert_one(data_dict)       

        hostname = socket.gethostname()        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        publisher.send(json.dumps({
            'thumbnail' : thumbnail_image.decode(), 'uuid':data_dict['uuid'],'timestamp':data_dict['timestamp'],
            'mac_address': data_dict['mac_address'],'ip': s.getsockname()[0] , 'objects': json.dumps(objects)
        }))
        s.close()
        time.sleep(1)
        os.remove(img)
    #wait for 1 minute
    time.sleep(2)