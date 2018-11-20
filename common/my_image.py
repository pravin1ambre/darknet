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
import requests

ImageFile.LOAD_TRUNCATED_IMAGES = True


publisher = DataPublisher()
from detectobject import detect_object

MONGO_HOST = 'localhost'
MONGO_PORT = '27017'
MONGO_DB = 'kkesani_3'
IMAGE_PATH = '/home/pravin/project/darknet/darknet/images/'
DATASCIENCE_IMAGE_PATH = '/home/pravin/data_science_images'
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

@exception
def process_and_save_image(img):
    data_dict = {'objects': ''}
    mac_address = "_".join(os.path.basename(img).split("_", 3)[:3])
    mac_address_exists = db.config.find_one({"mac_address": mac_address})
    print("Executing for {}".format(img))

    if mac_address_exists and mac_address_exists['object_sync']:
        data_dict['objects'] = json.dumps(detect_object(img))
        data_dict['prediction_image'] = image_to_str(
            "{}/predictions.jpg".format(os.getcwd()),
            typ="Prediction_image")

    if not mac_address_exists:
        data = {'mac_address': mac_address,
                'object_sync': False,
                'tag': 'tag',
                'source_sync': True,
                'thumbnail_sync': True,
                'prediction_sync': False,
                "creationTime": datetime.now(),
                }
        db.config.insert_one(data)

    data_dict['uuid'] = str(uuid.uuid1())
    data_dict['timestamp'] = int(time.time())
    data_dict['mac_address'] = mac_address
    data_dict['source'] = image_to_str(img)
    data_dict['thumbnail'] = resizeImage(img)
    data_dict['creationTime'] = datetime.now()
    db.timeseries_data.insert_one(data_dict)

    return data_dict

@exception
def send_image_info(data_dict):
    publisher = DataPublisher()
    publisher.send(json.dumps({
        'thumbnail': data_dict['thumbnail'].decode(),
        'uuid': data_dict['uuid'],
        'timestamp': data_dict['timestamp'],
        'mac_address': data_dict['mac_address'],
        'ip': requests.get("http://icanhazip.com").text.strip(),
        'objects': data_dict['objects']
    }))
    pass

@exception
def get_img_files():
    files_with_path = glob.glob(IMAGE_PATH + "/*")
    print("Got {} files on  {}".format(len(files_with_path), IMAGE_PATH))
    return files_with_path

if __name__ == '__main__':
    while True:
        for img in get_img_files():
            data_dict = process_and_save_image(img)
            send_image_info(data_dict)
            time.sleep(IMG_SLEEP_TIME)
            copy_path = "{}/{}".format(DATASCIENCE_IMAGE_PATH, str("".join(os.path.basename(img).split("_",2)[:2])))
            if not os.path.exists(copy_path):
                os.mkdir(copy_path)
            shutil.copy(img, copy_path)
            rename = str("_".join(os.path.basename(img).split("_",2)[:2]))+ str(int(time.time())) +'.jpg'
            os.rename(copy_path+"/"+ os.path.basename(img),copy_path+"/"+rename)
            os.remove(img)
        # wait for 1 minute
        time.sleep(PROCESS_SLEEP_TIME)