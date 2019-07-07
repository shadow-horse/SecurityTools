#!/usr/bin/python

import time
import json
import copy
from selenium import webdriver
from urllib.parse import urlparse
from urllib.parse import parse_qs

"""
动态抓取网页内容
"""
class DomxssScanner:
    def __init__(self):
        self.service_args = []
        self.service_args.append('--load-images=no')  #关闭图片加载
        self.service_args.append('--disk-cache=yes')  #开启缓存
        self.service_args.append('--ignore-ssl-errors=true') #忽略证书错误
        self.browser = webdriver.PhantomJS("/Users/snow/programs/phantomjs-2.1.1-macosx/bin/phantomjs",service_args=self.service_args)
        #explicit waits 和implicit wait 在获取element前，等待Ajax执行完毕
        self.browser.implicitly_wait(10)
        
    '''
    初始化
    '''
    def setUrl(self,url):
        self.url = url
        self.cookies = []

    
    def setCookies(self,domain,name,value):
        #清除Cookie
#       self.browser.get(self.url) 
#       self.browser.delete_all_cookies()
        cookie = {}
        cookie={
            'domain':'',
            'name':'',
            'value':'',
            'path':''
        }
        cookie['domain'] = domain
        cookie['name'] = name
        cookie['value'] = value
        cookie['path'] = '/'
        
        self.browser.add_cookie(cookie)
    '''
    扫描URL
    '''
    def scanUrl(self,payloads):
        
        script = "var page = this; page.onConsoleMessage = function(msg) {page.browserLog.push(msg);};"
        self.browser.command_executor._commands['executePhantomScript'] = ('POST', '/session/$sessionId/phantom/execute')
        self.browser.execute('executePhantomScript', {'script': script, 'args': []})
        
        #检测前抽取参数
        
        self.browser.get(self.url)  
        time.sleep(10) #直接设置等待10s
        
        self.pagesource = self.browser.page_source 
        self.requestlists = self.browser.get_log('browser')
#         print(self.pagesource)
    def dealUrl(self,url):
        #GET请求参数处理
        self.url = url
        url_parse = urlparse(self.url['url'])
        url_params = parse_qs(url_parse.query)
        url_postdata = parse_qs(self.url['postdata'])
        domain = url_parse.scheme + "://" + url_parse.netloc + url_parse.path
        
        #循环拼接参数
        if(self.url['method'] == 'GET' or self.url['method'] == 'get'):
            for p in url_postdata.keys():
                url_params[p] = url_postdata[p]
        
        #针对每一个参数，循环遍历payloads
        for param in url_params:
            temp_params = copy.deepcopy(url_params)
            for payload in self.payloads:
                payload = json.loads(payload)
                temp_params[param][0] = payload["poc"]
                newurl = self.spliceurl(domain,temp_params)
            
    def spliceurl(self,domain,params):
        url = domain
        url = url + "?"
        for p in params.keys():
            url = url + p + "=" + params[p][0] +"&"
        return url
    
    def setPayloads(self,payloads):     
        self.payloads = payloads