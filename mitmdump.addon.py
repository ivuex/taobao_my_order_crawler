# -*- coding:utf-8 -*-

import re
import json
from db import mongo
import pprint
# import time
# from mitmproxy import ctx

CORE_COLLECTION_NAME = 'core_my_history_order'
ORIGIN_COLLECTION_NAME = 'origin_my_history_order'

class PipeInbackend:
    def __init__(self):
        pass

    def response(self, flow):
        # 如果正则匹配上了flow.request.url就处理响应体，也可以用mitmproxy提供的flowfilter.parse和flowfilter.match
        if re.search(r'asyncBought.htm\?action', flow.request.url):
            json_str = flow.response.text
            match = re.search(r'&pageNum=(\d+)&', json_str)
            try:
                pageNum = match.group(1)
            except:
                print('Cannot found pageNum, some error ocurred.')

            # 保存原始数据

            # 写原始到文件中
            # JSON_PATH = 'jsons.d/{0:s}.order_list.json'.format(time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time())))
            ORIGIN_JSON_PATH = 'origin.jsons.d/{0:s}.origin_order_list.json'.format(pageNum)
            with open(ORIGIN_JSON_PATH, 'w') as f:
                f.write(json_str)

            # 保存原始数据到 mongodb
            data = json.loads(json_str)
            data['page_num'] = pageNum
            mongo.insert(ORIGIN_COLLECTION_NAME, data)

            # 获取关键数据
            core_data = self.parse(data)
            pprint.pprint(core_data, indent=2)
            print('{:<30}{:^10}{:>30}'.format('-'*30, '分割线', '-'*30))

            # 保存关键数据到文件中
            CORE_JSON_PATH = 'core.jsons.d/{0:s}.core_order_list.json'.format(pageNum)
            with open(CORE_JSON_PATH, 'w') as f:
                core_data_json_str = json.dumps(core_data)
                f.write(core_data_json_str)

            # 保存关键数据到 mongodb
            mongo.insert(CORE_COLLECTION_NAME, core_data)

    def parse(self, data):
        core_data = []
        for main_order in data['mainOrders']:
            id = main_order['id']
            seller_name = main_order['seller']['nick']
            create_time = main_order['orderInfo']['createTime']
            status_info = main_order['statusInfo']['text']
            sub_orders = []
            for sub in main_order['subOrders']:
                sub_order = {}
                sub_order['product_name'] = sub['itemInfo']['title']
                sub_order['price'] = sub['priceInfo']['realTotal']
                sub_orders.append(sub_order)
            order =  {
                'id': id,
                'seller_name': seller_name,
                'create_time': create_time,
                'status_info': status_info,
                'sub_orders': sub_orders,
            }
            core_data.append(order)
        return core_data



addons = [
    PipeInbackend()
]

