# -*- coding:utf-8 -*-
# from pymongo import MongoClient
from db import mongo
import sys
import json
from mitmproxy import flowfilter
import time
import requests

'''
匹配带订单记录响应体的请求，并将响应体转字典存mongodb
'''

class OrderFetcher:
    '''
    从抓包可以看到 问题包的链接最后是 findQuiz
    '''
    def __init__(self):
       self.filter = flowfilter.parse('~u buy.*asyncBought\.htm ~m post')
       # self.conn = MongoClient('45.249.94.149', 27017)
       # self.conn = MongoClient('127.0.0.1', 27017)
       # self.db = self.conn['taobao']
       # self.collection = self.db['my_history_order']
       #  pass

    def request(self, flow):
        '''
        演示request事件效果, 请求的时候输出提示
        :param flow:
        :return:
        '''
        # if flowfilter.match(self.filter,flow):
        #     ...

    def responseheaders(self, flow):
        '''
        演示responseheaders事件效果, 添加头信息
        :param flow:
        :return:
        '''
        # if flowfilter.match(self.filter, flow):
        #     flow.response.headers['Cache-Control'] = 'no-cache'
        #     flow.response.headers['Pragma'] = 'no-cache'
        # ...

    def response(self, flow):
        '''
        HTTPEvent 下面所有事件参数都是 flow 类型 HTTPFlow
        可以在API下面查到 HTTPFlow, 下面有一个属性response 类型 TTPResponse
        HTTPResponse 有个属性为 content 就是response在内容,更多属性可以查看 文档
        :param flow:
        :return:
        '''
        if flowfilter.match(self.filter, flow):
            json_str = flow.response.text
            self.pipe_to_mongodb(json_str)
            self.pipe_to_file(json_str)

    def pipe_to_file(self, json_str):
        JSON_PATH = 'jsons.d/{0:s}.order_list.json'.format(time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time())))
        with open(JSON_PATH, 'w') as f:
            f.write(json_str)

    def pipe_to_mongodb(self, json_str):
        data = json.loads(json_str)
        mongo.insert(data)
        # requests.post('http://localhost:5000/save2db', data=data)
        # d = json.loads(json_str)
        # print
        # self.collection.insert(d)


#这里简单演示下start事件
def start():
    return OrderFetcher()


