# -*- coding:utf-8 -*-

import requests
import re
import json
import time
from random import choice, randint
from prettytable import PrettyTable
import os
# import progressbar

import Configure

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

header = {}
header['user-agent'] = choice(Configure.FakeUserAgents)
header['referer'] = 'https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm'

cookies = {}
cookiestr = '''
			isg=BKOjhWKq-5VY4Leh_VZLneEGMuGNMF2_e_k4mdUA7YJHFMM2XWjHKoHGCuUatI_S;cookie17=VvqkSn0i%2Fq0I;_nk_=tb3170299;thw=us;dnk=tb3170299;lgc=tb3170299;tg=0;_cc_=URm48syIZQ%3D%3D;_tb_token_=fee3056579376;uc3=vt3=F8dByRMCRNjxWOQ9s3A%3D&id2=VvqkSn0i%2Fq0I&nk2=F5RGNw%2Bct87t&lg2=UIHiLt3xD8xYTw%3D%3D;v=0;csg=e7eadf56;tracknick=tb3170299;cookie1=VAFX453MLqZPCFzpEZ0QttfTWIIC7VjQI%2B%2BJY1%2F4SDU%3D;publishItemObj=Ng%3D%3D;skt=8da84e8a5d5f8cdf;sg=919;l=aBfQC2UYyHZCtoQmyMaY8lrm8xrxygBzfT-X1MaztiYGdP8vK6rO1jno-Vwyd_qC5f9y_KniI;uc1=cookie14=UoTYM8NFEtY30A%3D%3D&lng=zh_CN&cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&existShop=false&cookie21=URm48syIZJfmYzXkqdDvJg%3D%3D&tag=8&cookie15=WqG3DMC9VAQiUQ%3D%3D&pas=0;_l_g_=Ug%3D%3D;mt=ci=12_1;cna=ZSamFM/p5xICAS35XpX8Pj3o;existShop=MTU0NTU1MDI0Mw%3D%3D;hng=CN%7Czh-CN%7CCNY;unb=542827051;cookie2=12fc06cd141ba143945a4814a88c8129;t=8621073fe1d748631a4ad2b601906bb1
			'''


# print(cookies, '36-36', 'cookies')

# 设置代理
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--proxy-server=http://localhost:8080")
# 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
# browser = webdriver.Chrome()
browser = webdriver.Chrome(chrome_options = chromeOptions)

wait = WebDriverWait(browser, 20)
browser.get('https://www.taobao.com')


COOKIES_FILE_PATH = 'cookies.txt'

init_url = "https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm"
#这里请求这个初始化url，是为了避免下边第一次获取cookies报错
browser.get(init_url)
def set_cookie_from_file_if_exist():
    if os.path.exists(COOKIES_FILE_PATH):
        with open(COOKIES_FILE_PATH, 'r') as f:
            cookiestr = f.read()
        if not cookiestr.strip():
            return
        for cookie in cookiestr.split(';'):
            name, value = cookie.strip().split('=', 1)
            browser.add_cookie({'name':name, 'value':value, 'domain':'.taobao.com'})
set_cookie_from_file_if_exist()

def write_logined_cookies_into_file_if_updated():
    cookies = browser.get_cookies()
    cookiesStr = ""
    for cookie in cookies:
        cookiesStr += cookie.get('name') + '=' + cookie.get('value') + ';'

    if cookiesStr.strip():
        cookiesStr = cookiesStr[:-1]
        # cookies_file_path = 'cookies.d/{0:s}.cookies.txt'.format(time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time())))

        with open(COOKIES_FILE_PATH, 'r') as f:
            if cookiestr == f.read():
                print('cookies is the same as one in the cookies file.')
                return
        with open(COOKIES_FILE_PATH, 'w') as f:
            f.write(cookiesStr)
            print('cookies was updated into {0:s}, the content is {1:s}'.format(COOKIES_FILE_PATH, cookiestr));
    # print(res)


def selenium_makesure_logined():
    while True:
        if browser.current_url.startswith("https://login.taobao.com"):
            try:
                refresh = browser.find_element_by_class_name('J_QRCodeRefresh')
                refresh.click()
            except:
                print('Please make sure the J_QRCodeRefresh is not out of expired, and use taobao mobile client to scan the J_QRCodeRefresh code, then wait for the page being redirect if it would. ')
                time.sleep(4)
        else:
            write_logined_cookies_into_file_if_updated()
            print('The browser has been already logined yet.')
            break


page_total = 50
# bar = progressbar.ProgressBar(maxval=page_total).start()
page_nums = list(range(1, page_total + 1)) #总共有50页

def getOnePageOrderHistory():

    # global nextpagenum

    randnum = randint(1, len(page_nums))
    nextpagenum = page_nums[randnum - 1]


    # 验证码通过后，新的URL后面会带Token值
    # 带着这个值才能访问成功，并且访问下个页面不再需要验证码
    # newURL就是通过验证后的新URL
    # if newURL:
    #     url = newURL

    selenium_makesure_logined()
    # msg = dri
    # if not driver.findElement
    #    return getOnePageOrderHistory()


    print("抓取第{0:d}页".format(nextpagenum))

    # orders = browser.find_elements_by_css_selector('table.bought-table-mod__table___3u4gN.bought-wrapper-mod__table___3xFFM')
    #
    # table = PrettyTable()
    # table.field_names = ["ID", "卖家", "商品名称", "订单创建时间", "价格", "状态"]
    #
    # browser.execute_script('''
    #     idEles = [].slice.call(
    #         document.querySelectorAll('tbody:nth-child(2) tr:nth-child(1) td:nth-child(1) span:nth-child(2) > span:nth-child(3)')
    #         )
    #     ids = idEles.map(item => item.innerText)
    #     nextpagenum = document.querySelector('.pagination-options-quick-jumper input').value
    #     console.log(ids, nextpagenum)
    # ''')
    #
    # for order in orders:
    #     # print(order)
    #     row = []
    #     row.append(order.find_element_by_css_selector('body.bought.mytaobao-v2:nth-child(2) div.grid-c2:nth-child(1) div.col-main div   tr:nth-child(1) td span:nth-child(2) > span:nth-child(3)').text) # id
    #
    #     row.append(order.find_element_by_css_selector('.seller-mod__name___37vL8').text) # 卖家
    #     # good = order.find_element_by_css_selector('table.bought-table-mod__table___3u4gN.bought-wrapper-mod__table___3xFFM tbody:nth-child(3)')
    #     row.append(order.find_element_by_css_selector('td.sol-mod__no-br___1PwLO  div:nth-child(2) p:nth-child(1) a:nth-child(1) > span:nth-child(2)').text) # 商品名称
    #     row.append(order.find_element_by_css_selector('tbody.bought-wrapper-mod__head___2vnqo:nth-child(2) tr:nth-child(1) td.bought-wrapper-mod__head-info-cell___29cDO:nth-child(1) label.bought-wrapper-mod__checkbox-label___3Va60:nth-child(1) > span.bought-wrapper-mod__create-time___yNWVS').text) # 订单创建时间
    #     row.append(order.find_element_by_css_selector('div:nth-child(1) div.price-mod__price___157jz:nth-child(1) p:nth-child(1) strong:nth-child(1) > span:nth-child(2)').text) # 价格
    #     row.append(order.find_element_by_css_selector('tr:nth-child(1) td:nth-child(6) div:nth-child(1) p:nth-child(1) > span.text-mod__link___1dpU2').text) # 状态
    #     table.add_row(row)
    # print(table)

    # print('105-105', 'table')

    # nextpage = browser.find_element_by_css_selector('li.pagination-next:nth-child(9)')
    # nextpage = browser.find_element_by_css_selector('button.button-mod__button___ci6-a.button-mod__default___iyi1-.button-mod__small___1ugIJ:nth-child(2)')
    # next_css_selector = '.pagination-item-{0:d}'.format(pagenum + 1)
    # nextpage = browser.find_element_by_css_selector(next_css_selector)
    # print(next_css_selector, '96-96', 'next_css_selector')
    # nextpage = browser.find_element_by_css_selector('.pagination-item-3')


    # randnum = randint(0,50)
    # nextpagenum = randnum

    page_input = browser.find_element_by_css_selector('.pagination-options-quick-jumper input')
    page_input.clear()
    page_input.send_keys(nextpagenum)
    go = browser.find_element_by_css_selector('span.pagination-options-go')
    action = ActionChains(browser)
    action.reset_actions()
    # action.move_to_element(nextpage)
    action.move_to_element(go)
    action.move_by_offset(10, -10).click()
    action.perform()


    try:
        browser.execute_script('document.documentElement.scrollTop = {0:d}'.format(2050 + randint(50, 150)))

        # nextpage.click()

        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.pagination-item-{0:d}.pagination-item-active'.format(nextpagenum)))
        )
        # 请求成功就将该页码弹出
        page_nums.pop(randnum - 1)
    except TimeoutException:
        print('没有更多列订单表分页，或者获取新的分页超时')
    # pagenum += 1
    print('remain pages: ', page_nums)
    # bar.update(nextpagenum)

    time.sleep(7)
    if len(page_nums):
        getOnePageOrderHistory()


# 打印订单信息
def getOrderDetails(data):
    table = PrettyTable()
    table.field_names = ["ID", "卖家", "商品名称", "订单创建时间", "价格", "状态"]

    for order in data:
        tmp = []
        # id =
        tmp.append(order.get('id'))
        # shopName
        tmp.append(order.get('seller').get('shopName'))
        # title
        tmp.append(order.get('subOrders')[0].get('itemInfo').get('title'))
        # createTime
        tmp.append(order.get('orderInfo').get('createTime'))
        # actualFee
        tmp.append(order.get('payInfo').get('actualFee'))
        # text
        tmp.append(order.get('statusInfo').get('text'))

        table.add_row(tmp)

    print(table)


# def passCodeCheck(referer_url, pageNum):
#     # 在url中插入style=mini获取包含后续要用到的所有参数的页面
#     url = referer_url.replace("?", "?style=mini&")
#
#     try:
#         response = requests.post(url, headers=header, cookies=cookies)
#         content = None
#
#         if response.status_code == requests.codes.ok:
#             content = response.text
#
#     except Exception as e:
#         print(e)
#
#     # 获取identity, sessionid和type
#     pattern = re.compile(
#         'new Checkcode\({.*?identity: \'(.*?)\''
#         '.*?sessionid: \'(.*?)\''
#         '.*?type: \'(.*?)\'.*?}\)', re.S)
#     data = pattern.findall(content)
#
#     m_identity = data[0][0]
#     m_sessionid = data[0][1]
#     m_type = data[0][2]
#
#     # 获取action, m_event_submit_do_unique, m_smPolicy
#     # m_smApp, m_smReturn, m_smCharset, smTag
#     # captcha和smSign
#     pattern = re.compile(
#         'data: {'
#         '.*?action: \'(.*?)\''
#         '.*?event_submit_do_unique: \'(.*?)\''
#         '.*?smPolicy: \'(.*?)\''
#         '.*?smApp: \'(.*?)\''
#         '.*?smReturn: \'(.*?)\''
#         '.*?smCharset: \'(.*?)\''
#         '.*?smTag: \'(.*?)\''
#         '.*?captcha: \'(.*?)\''
#         '.*?smSign: \'(.*?)\',', re.S)
#     data = pattern.findall(content)
#
#     m_action = data[0][0]
#     m_event_submit_do_unique = data[0][1]
#     m_smPolicy = data[0][2]
#     m_smApp = data[0][3]
#     m_smReturn = data[0][4]
#     m_smCharset = data[0][5]
#     m_smTag = data[0][6]
#     m_captcha = data[0][7]
#     m_smSign = data[0][8]
#
#     # 处理验证码
#     res = False
#     m_code = ""
#     while res == False:
#         res, m_code = checkCode(m_identity, m_sessionid, m_type, url)
#
#     # 构建URL，获取最后的Token
#     murl = "https://sec.taobao.com/query.htm"
#
#     mheader = {}
#     mheader['user-agent'] = choice(Configure.FakeUserAgents)
#     mheader['referer'] = url
#
#     mpayload = {
#         'action': m_action,
#         'event_submit_do_unique': m_event_submit_do_unique,
#         'smPolicy': m_smPolicy,
#         'smApp': m_smApp,
#         'smReturn': m_smReturn,
#         'smCharset': m_smCharset,
#         'smTag': m_smTag,
#         'captcha': m_captcha,
#         'smSign': m_smSign,
#         'ua': getUA(),  # 获取最新的UA
#         'identity': m_identity,
#         'code': m_code,
#         '_ksTS': '{0:d}_39'.format(int(time.time() * 1000)),
#         'callback': 'jsonp40'
#     }
#
#     try:
#         response = requests.get(murl, headers=mheader, params=mpayload, cookies=cookies)
#         content = None
#
#         if response.status_code == requests.codes.ok:
#             content = response.text
#
#     except Exception as e:
#         print(e)
#
#     pattern = re.compile('{(.*?)}', re.S)
#     data = pattern.findall(content)
#     jsond = json.loads('{' + data[0] + '}')
#
#     # 这个json文件里包含了最后访问用的URL
#     murl = jsond.get('url')
#     getOnePageOrderHistory(pageNum, murl)


# def checkCode(m_identity, m_sessionid, m_type, url):
#     # 获取验证码的图片
#     murl = "https://pin.aliyun.com/get_img"
#
#     mheader = {}
#     mheader['user-agent'] = choice(Configure.FakeUserAgents)
#     mheader['referer'] = url
#
#     mpayload = {
#         'identity': m_identity,
#         'sessionid': m_sessionid,
#         'type': m_type,
#         't': int(time.time() * 1000)
#     }
#
#     try:
#         response = requests.get(murl, headers=mheader, params=mpayload, cookies=cookies)
#         content = None
#
#         if response.status_code == requests.codes.ok:
#             content = response.content
#
#     except Exception as e:
#         print(e)
#
#     # 将验证码图片写入本地
#     with open("codeimg.jpg", "wb") as file:
#         file.write(content)
#
#     # 输入并验证验证码
#     code = input("请输入验证码：")
#
#     murl = "https://pin.aliyun.com/check_img"
#
#     mpayload = {
#         'identity': m_identity,
#         'sessionid': m_sessionid,
#         'type': m_type,
#         'code': code,
#         '_ksTS': '{0:d}_29'.format(int(time.time() * 1000)),
#         'callback': 'jsonp30',
#         'delflag': 0
#     }
#
#     try:
#         response = requests.get(murl, headers=mheader, params=mpayload, cookies=cookies)
#         content = None
#
#         if response.status_code == requests.codes.ok:
#             content = response.text
#
#     except Exception as e:
#         print(e)
#
#     # 检测是否成功
#     # 这里要返回这个验证码，后面会用到
#     pattern = re.compile("SUCCESS", re.S)
#     data = pattern.findall(content)
#
#     if data:
#         return True, code
#     else:
#         return False, code


# def getUA():
#     # 利用PhantomJS模拟浏览器行为
#     # 访问本地的js文件来获取UA
#     driver = webdriver.PhantomJS()
#     driver.get("file:///D:/OneDrive/Documents/Python%E5%92%8C%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98/code/taobao/ua.html")
#     content = driver.find_element_by_tag_name('p').text
#     driver.close()
#
#     return content


if __name__ == '__main__':
    # for i in range(2, 25):
    # for i in range(1):
    getOnePageOrderHistory()
    time.sleep(2)

