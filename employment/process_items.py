#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import redis
import pymongo


def main():
    # r = redis.Redis()
    r = redis.Redis(host='192.168.1.139',port=6379,db=0)
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client['lagou']
    sheet = db['data3']

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
