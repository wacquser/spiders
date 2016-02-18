import pymongo
import time

client = pymongo.MongoClient('localhost', 27017)
db = client['lagou']
col = db['data']

while True:
    print col.count()
    time.sleep(2)