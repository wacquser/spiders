#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import redis
import pymongo
import time


def main():
    # r = redis.Redis()
    today = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
    # r = redis.Redis(host='192.168.1.139',port=6379,db=0)
    r = redis.Redis(host='127.0.0.1',port=6379,db=0)
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client['lagou']
    sheet = db[today]

    while True:
        # process queue as FIFO, change `blpop` to `brpop` to process as LIFO
        source, data = r.blpop(["lagou:items"])
        item = json.loads(data)
        sheet.insert(item)

        # try:
        #     print u"Processing: %(name)s <%(link)s>" % item
        # except KeyError:
        #     print u"Error procesing: %r" % item


if __name__ == '__main__':
    main()
