#!/usr/bin/python

#!/usr/bin/python

from spider import StaticSpider
from spider import DynamicSpider
from scanner import DomxssScanner
from tools import Deldump
from tools import FileOperation
from copy import deepcopy
from asyncio.tasks import sleep
import json

class SpiderOperation:
    
    '''
    初始化
    '''
    def init(self,deep,url):
        self.deep = deep
        self.url = url 
        self.urllists = []   #保存所有的扫描结果
        self.currenturls = []   #当前层的扫描结果
        self.nexturls = []  #下一层的扫描结果
        self.urlsnums = 0
        self.lasttime = 0
        self.currentdeep = 0
    
    '''
    每开始扫描一条URL，则打印一次时间，通过剩余的URL计算剩余时间
    每条URL扫描的平均时间为20s(暂定)
    打印一次，次数减少一次
    '''
    def printLasttime(self):
        eachtime = 20
        seconds = self.urlsnums * eachtime
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        print ("爬虫剩余时间:    %02d:%02d:%02d" % (h, m, s))
        self.urlsnums = self.urlsnums - 1
    
    '''
    汇总urls，将扫描的扫描添加到所有的链接中
    添加到下一层链接中
    '''
    def addUrls(self,data):
        for d in data:
            self.urllists.append(d)
            self.nexturls.append(d['url'])
            if(self.currentdeep < self.deep):
                self.urlsnums = self.urlsnums + 1
            print("新增链接: %s" % (d['url']))
    
    def getUrls(self):
        #去重
        delDump = Deldump.Deldump()
        result = delDump.deldumpurls(self.urllists)
        return result
    '''
    静态爬虫、动态排重  
    爬虫深度
    打印剩余时间
    未及时去重，导致爬虫可能会浪费时间
    递归爬虫仅仅爬取GET请求，不处理POST请求，POST请求相对页面跳转比较少
    '''
    def startSpider(self):
        #初始化句柄
        self.spiderInit()
        #初始化下一层的扫描
        self.nexturls.append(self.url)
        self.urlsnums = 1
        for i in range(self.deep):
            # 保存当前深度，计算剩余时间
            self.currentdeep = i + 1
            # 开始扫描，将下一层的urls赋值为当前层
            self.currenturls = deepcopy(self.nexturls)
            # 清空下一层
            self.nexturls = []
            #执行当前层的扫描
            for url in self.currenturls:
                self.printLasttime()
                self.staticSpider(url)
                self.dynamicSpider(url)
                
    '''
    爬虫创建全局的句柄，是的只需要加载一次 
    '''
    def spiderInit(self):
        self.staticspider = StaticSpider.StaticSpider()
        self.dynamicspider = DynamicSpider.DynamicSpider()
        
    def staticSpider(self,url):
        self.staticspider.setUrl(url)
        self.staticspider.parseHtml()
        self.staticspider.getHrefs()
        self.staticspider.getFormurls()
        surls = self.staticspider.getUrls()
        self.addUrls(surls)
        
    
    def dynamicSpider(self,url):
        self.dynamicspider.setUrl(url)
        self.dynamicspider.loadAsynHtml()
        self.dynamicspider.getClickButtonsurls()
        durls = self.dynamicspider.getUrls()
        self.addUrls(durls)
    
        
        url = "http://127.0.0.1:8080/web/index.html"
    
    print("############静态爬虫#############")
    
    
