#!/usr/bin/python

import time
import json
from selenium import webdriver


"""
动态抓取网页内容
"""
class DynamicSpider:
    def __init__(self):
        self.service_args = []
        self.service_args.append('--load-images=no')  #关闭图片加载
        self.service_args.append('--disk-cache=no')  #开启缓存
        self.service_args.append('--ignore-ssl-errors=true') #忽略证书错误
        self.browser = webdriver.PhantomJS("/Users/snow/programs/phantomjs-2.1.1-macosx/bin/phantomjs",service_args=self.service_args)
        #explicit waits 和implicit wait 在获取element前，等待Ajax执行完毕
        self.browser.implicitly_wait(10)
        
    '''
    初始化
    '''
    def setUrl(self,url):
        self.url = url
        
    '''
    加载异步请求页面
    '''
    def loadAsynHtml(self):
        #script脚本，通过onResourceRequested获取发起的请求
        script = "var page = this; page.onResourceRequested  = function(request) {page.browserLog.push(JSON.stringify(request));};"
        self.browser.command_executor._commands['executePhantomScript'] = ('POST','/session/$sessionId/phantom/execute')
        self.browser.execute('executePhantomScript', {'script': script, 'args': []})
        
        self.browser.get(self.url)  
        time.sleep(10) #直接设置等待10s
        self.pagesource = self.browser.page_source 
        #获取browser log内容，我们将获取到的信息写入了browser log，目前不知道是否还有其它获取内容的API接口
        self.requestlists = self.browser.get_log('browser')
        
    def getHtmltext(self):
        return self.pagesource
    
    '''
    获取request list，处理数据格式，获取有效的请求
    '''
    def getRequestlists(self):
        self.reqlists = []
        id = 1
        for req in self.requestlists:
            json_object = json.loads(req)
            reqinfo = {}
            if(json_object['method'] == 'GET'):
                reqinfo['id'] = id
                reqinfo['method'] = json_object['method']
                reqinfo['url'] = json_object['url']
                reqinfo['postdata'] = ''
            else:
                reqinfo['id'] = id
                reqinfo['method'] = json_object['method']
                reqinfo['url'] = json_object['url']
                reqinfo['postdata'] = json_object['postData']
            self.reqlists.append(reqinfo)
            id = id + 1    
        return self.reqlists