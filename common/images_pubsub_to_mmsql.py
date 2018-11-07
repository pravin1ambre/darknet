from publisher_subscriber import DataConsumer
import pymysql
import json, time
import base64
import datetime, os


def fetch_image(image_str, mac_address):
    # fh = open(/home/EOG/kkesani/fetched_images/{}.jpg".format(count), "wb")
    name = str(datetime.datetime.now()).replace(' ', '-').replace(":","_")
    # filepath = "C:\\Users\\kkesani\\Desktop\\output\\{}".format(PRIMO_ID)
    filepath = "/home/EOG/kkesani/fetched_images/{}".format(mac_address)
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    complete_path = "{}/{}.jpg".format(filepath, name)
    # fh = open("{}\\{}.jpg".format(filepath, name), "wb")
    fh = open(complete_path, "wb")
    fh.write(base64.b64decode(image_str))
    fh.close()
    print(complete_path,"--------------complete---path------------")
    return complete_path

class PubSubToDataBase(object):
    def __init__(self, host, user, password, db):
        self.conn = pymysql.connect(host=host, user=user, passwd=password, db=db)
        self.cur = self.conn.cursor()
        self.LC = DataConsumer()

    def execute(self, console_display = True):
        print("waiting for messages...")
        while True:
            print(self.LC.queue.qsize())
            while self.LC.queue.qsize()>0:
                message = self.LC.get_messages()
                payload_dict = json.loads(message.decode('utf-8'))
                payload = json.loads(payload_dict.get('payload'))
                detected_objects = payload.get('objects') # json.dumps(json.loads())

                print(detected_objects,type(detected_objects))
                timestamp = payload.get('timestamp')
                uuid = payload.get('uuid')            
                tumbnail= payload.get('thumbnail')
                bb_hostname = payload.get('ip')
                cam_mac_address = payload.get('mac_address')
                # detected_objects = payload.get('objects')                
                thumbnail_filepath = fetch_image(tumbnail, cam_mac_address) 
                sql = "select (1) from camera_image where uuid = %s limit 1"
                val =(uuid)
                if self.cur.execute(sql, val):
                    sql = "UPDATE camera_image SET detected_objects = %s WHERE uuid = %s"
                    val = (detected_objects, uuid)
                else:
                    sql = 'Insert into camera_image(detected_objects,thumbnail_filepath,cam_mac_address, bb_hostname,timestamp,uuid,created_at)values(%s,%s,%s,%s, %s, %s, now())'
                    val = (detected_objects,thumbnail_filepath,cam_mac_address, bb_hostname ,timestamp,uuid)
                self.cur.execute(sql, val)
                self.conn.commit()

            time.sleep(5)
if __name__ == "__main__":
   PubSubToDataBase(host='ktyvlxmsqlio01', user='root', password='hiVcgidXgiy2VABA3Ptu', db='camera_images').execute()
