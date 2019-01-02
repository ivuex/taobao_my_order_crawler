# -*- coding:utf-8 -*-

import requests
import re
import json
import time
from random import choice, randint
# from prettytable import PrettyTable
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
'''
taobao.com的cookies每次通过登陆都会被更新
这里初始化cookies，如果能拿到最新登陆的cookie，可以把新cookie粘过来
'''
cookiestr = '''
			isg=BKOjhWKq-5VY4Leh_VZLneEGMuGNMF2_e_k4mdUA7YJHFMM2XWjHKoHGCuUatI_S;cookie17=VvqkSn0i%2Fq0I;_nk_=tb3170299;thw=us;dnk=tb3170299;lgc=tb3170299;tg=0;_cc_=URm48syIZQ%3D%3D;_tb_token_=fee3056579376;uc3=vt3=F8dByRMCRNjxWOQ9s3A%3D&id2=VvqkSn0i%2Fq0I&nk2=F5RGNw%2Bct87t&lg2=UIHiLt3xD8xYTw%3D%3D;v=0;csg=e7eadf56;tracknick=tb3170299;cookie1=VAFX453MLqZPCFzpEZ0QttfTWIIC7VjQI%2B%2BJY1%2F4SDU%3D;publishItemObj=Ng%3D%3D;skt=8da84e8a5d5f8cdf;sg=919;l=aBfQC2UYyHZCtoQmyMaY8lrm8xrxygBzfT-X1MaztiYGdP8vK6rO1jno-Vwyd_qC5f9y_KniI;uc1=cookie14=UoTYM8NFEtY30A%3D%3D&lng=zh_CN&cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&existShop=false&cookie21=URm48syIZJfmYzXkqdDvJg%3D%3D&tag=8&cookie15=WqG3DMC9VAQiUQ%3D%3D&pas=0;_l_g_=Ug%3D%3D;mt=ci=12_1;cna=ZSamFM/p5xICAS35XpX8Pj3o;existShop=MTU0NTU1MDI0Mw%3D%3D;hng=CN%7Czh-CN%7CCNY;unb=542827051;cookie2=12fc06cd141ba143945a4814a88c8129;t=8621073fe1d748631a4ad2b601906bb1
			'''


# print(cookies, '36-36', 'cookies')

# 设置代理
chromeOptions = webdriver.ChromeOptions()
# mitmproxy默认监听8080端口，这里配置浏览器代理为mitmproxy
# 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://localhost:8080
chromeOptions.add_argument("--proxy-server=http://localhost:8080")
# 加载配置，并赋值给browser变量
browser = webdriver.Chrome(chrome_options = chromeOptions)
# 配置超时最大等待时间
wait = WebDriverWait(browser, 20)

# cookies将为被拼接后写到这个路径里
COOKIES_FILE_PATH = 'cookies.txt'

# 设置初始url
init_url = "https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm"
#这里请求这个初始化url，是为了避免下边第一次获取cookies报错
browser.get(init_url)

# 如果COOKIES_FILE_PATH文件存在，并且内容不为空并且不是空字符串就读取，并解析后添加到浏览器cookies里
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


# 如果浏览器获取到了cookies就保存到COOKIES_FILE_PATH里
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

# 如果淘宝的机制判断需要登陆，就切换出扫码原始(避免淘宝无敌[机器学习判断是否爬虫的]的极验验证码)，轮询等待扫码
def selenium_makesure_logined():
    while True:
        # 如果当前url以"https://login.taobao.com"开头就说明需要登陆了
        if browser.current_url.startswith("https://login.taobao.com"):
            try:
                qr = browser.find_element_by_class_name('J_QRCodeRefresh')
                qr.click()
            except:
                print('Please make sure the J_QRCodeRefresh is not out of expired, and use taobao mobile client to scan the J_QRCodeRefresh code, then wait for the page being redirect if it would. ')
                time.sleep(4)
        else:
            # 登陆成功了就把cookies写到COOKIES_FILE_PATH里
            write_logined_cookies_into_file_if_updated()
            print('The browser has been already logined yet.')
            break



#总共有50页
page_total = 50
page_nums = list(range(1, page_total + 1))

def getHistoryOrder():

    # 获取随机索引
    randnum = randint(1, len(page_nums))
    # 随机获取还需要爬取的页数
    nextpagenum = page_nums[randnum - 1]

    # 确保已经登陆过了
    selenium_makesure_logined()

    # 滚动到分页的浏览器滚出高度 用randint模拟人每次滚动位置不同
    browser.execute_script('document.documentElement.scrollTop = {0:d}'.format(2050 + randint(50, 150)))

    print("抓取第{0:d}页".format(nextpagenum))

    # 直接点击下一页，或者点击页码 都会遇到一些莫名其妙的问题，所以键入页码并转跳
    page_input = browser.find_element_by_css_selector('.pagination-options-quick-jumper input')
    page_input.clear()
    page_input.send_keys(nextpagenum)
    go = browser.find_element_by_css_selector('span.pagination-options-go')
    # 控制鼠标点击转跳按钮 有鼠标事件通常比 element.click() 兼容性要好(其实是避免被反爬)
    action = ActionChains(browser)
    action.reset_actions()
    action.move_to_element(go)
    action.move_by_offset(10, -10).click()
    action.perform()


    # 如果超时之前nextpagenum页不变为活动页，那么就是流程（多半是请求）出现了问题
    try:
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

    # 冷却一下，避免过频访问
    time.sleep(5)
    if len(page_nums):
        getHistoryOrder()

if __name__ == '__main__':
    getHistoryOrder()

