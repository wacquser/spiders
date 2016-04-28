import pymongo
import time

client = pymongo.MongoClient('localhost', 27017)
db = client['lagou']

import time
today = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
col = db[today]
print today
while True:
    print col.count()
    time.sleep(2)