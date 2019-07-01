#!/usr/bin/python

import time
from selenium import webdriver

"""
动态抓取网页内容
"""
class DynamicSpider:
    def __init__(self):
        self.browser = webdriver.PhantomJS("/Users/snow/programs/phantomjs-2.1.1-macosx/bin/phantomjs")
        #explicit waits 和implicit wait 在获取element前，等待Ajax执行完毕
        self.browser.implicitly_wait(10)
    '''
    初始化
    '''
    def setUrl(self,url):
        self.url = url
        
    '''
    获取异步请求加载完成后的页面
    '''
    def getAsynHtmltext(self):
        self.browser.get(self.url)  
        #time.sleep(10) 直接设置等待10s
        return self.browser.page_source
