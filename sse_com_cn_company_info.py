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
header['referer'] = 'http://listxbrl.sse.com.cn/companyInfo/toCompanyInfo.do?stock_id=600000&report_period_id=5000'







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

