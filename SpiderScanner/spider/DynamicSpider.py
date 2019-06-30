#!/usr/bin/python

from selenium import webdriver

"""
动态抓取网页内容
"""
class DynamicSpider:
    def __init__(self):
        self.browser = webdriver.PhantomJS("/Users/snow/programs/phantomjs-2.1.1-macosx/bin/phantomjs")
        
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
        return self.browser.page_source
