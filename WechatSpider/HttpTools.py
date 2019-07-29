#!/usr/bin/python

import requests
import urllib3
from selenium import webdriver
import warnings
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


'''
    封装HTTP/HTTPS请求，通用使用
'''

class HttpTools:
    
    def __init__(self,url,domain,cookies={},headers={},verify=False):
        self.url = url
        self.cookies = cookies
        self.headers = headers
        self.domain = domain
        #屏蔽SSL告警
        urllib3.disable_warnings()
        #设置重连次数
        requests.adapters.DEFAULT_RETRIES = 5  
        #关闭SSL证书验证
        self.verify = verify
     
    '''
    说明：
        使用动态浏览器加载页面时，必须初始化
    '''
    def initdynamic(self):
        warnings.filterwarnings("ignore")
        self.service_args = []
        self.service_args.append('--load-images=no')  #关闭图片加载
        self.service_args.append('--disk-cache=yes')  #开启缓存
        self.service_args.append('--ignore-ssl-errors=true') #忽略证书错误
        #设置请求头
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        for header in self.headers:
            dcap[header] = self.headers[header]
            
        self.browser = webdriver.PhantomJS("/Users/snow/programs/phantomjs-2.1.1-macosx/bin/phantomjs",service_args=self.service_args,desired_capabilities=dcap)
        #explicit waits 和implicit wait 在获取element前，等待Ajax执行完毕
        self.browser.implicitly_wait(3)
        
    #封装Get请求   
    def getRequest(self):
        try:
            res = requests.get(self.url,cookies = self.cookies,headers = self.headers,verify=self.verify)
            res.raise_for_status()
            res.encoding = res.apparent_encoding
            self.htmltext = res.text
            return self.htmltext
        except Exception as e:
            print (str(e))
            print("[error] Get "+self.url +" error.")
        
    
    #封装动态加载Get请求
    def dynamicGetRequest(self):
        #设置Cookie
        self.browser.get(self.url)
        self.browser.delete_all_cookies()
        for cookie in self.cookies:
            c = {'domain':'','path':'','name':'','value':''}
            c['domain']=self.domain
            c['path']='/'
            c['name'] = cookie
            c['value'] = self.cookies[cookie]
            self.browser.add_cookie(c)
        
        self.browser.get(self.url)
        time.sleep(3)
        reshtml = self.browser.page_source
        return reshtml   