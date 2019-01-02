# -*- coding:utf-8 -*-
import sys
sys.path.append('/Users/apple/.virtualenvs/py3crawl_modules_installation/lib/python3.7/site-packages')
from pymongo import MongoClient

conn = MongoClient('127.0.0.1', 27017)
db = conn['taobao']

class mongo():
    def insert(collection_name, data):
        # print(data)
        collection = db[collection_name]
        collection.insert(data)

