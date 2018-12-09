# #csv content read
from zipfile import ZipFile
zf = ZipFile('HP444 Cobalt 32 State 707H TDI-712-MLA01-012 - output data.csv.zip', 'r')
zf.extractall('/home/pravin/confidential/')
zf.close()
import datetime, os


# csv_data =  open('HP444 Cobalt 32 State 707H TDI-712-MLA01-012 - output data.csv','r')
# line = csv_data.readline()
# count = 0
mapping_file = open('54.txt','r') 
data = mapping_file.readlines()
keys = []
for da in data:
    ta = da.split("\t\t")
    keys.append(ta[2].split('\t\r\n')[0])
# print(keys)

# while line:
#     if not line[0] == '#':
#         count += 1
#         if count ==1:
#             mapping_key = line.split(" ")
#             match = set(mapping_key) & set (keys)
#             print(match)
#             # for k in keys:
#             #     print (k)
#     line = csv_data.readline()
    
import csv
import MySQLdb

mydb = MySQLdb.connect(host='localhost',
    user='root',
    passwd='admin',
    db='test')
cursor = mydb.cursor()
count = 0
csv_data = csv.reader(file('HP444 Cobalt 32 State 707H TDI-712-MLA01-012 - output data.csv'))
for row in csv_data:
    if not '#' in row[0]:
        if count:
            cnt = 0
            for r in row[2:]:
                print row
                try: 
                    key = keys[cnt]
                except:
                    key = None  
                cnt +=1   
                cursor.execute('INSERT INTO csvdata(Date, Time,matrics,value,timestamp) VALUES("{}", "{}", "{}","{}","{}")'.format(row[0],row[1],key,r,datetime.datetime.now()))
        count += 1
        
#close the connection to the database.
mydb.commit()
cursor.close()


