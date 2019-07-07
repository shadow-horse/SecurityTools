#!/usr/bin/python

from spider import StaticSpider
from spider import DynamicSpider
from scanner import DomxssScanner
from tools import Deldump
from tools import FileOperation
from spider import SpiderOperation
from test.test_decimal import file

def test1():    
    print("#####################################")
    
    a = "acadae"
    print(a.endswith("a"))
    
    
    url = "http://127.0.0.1:8080/web/index.html"
    
    print("############静态爬虫#############")
    staticspider = StaticSpider.StaticSpider()
    staticspider.setUrl(url)
    staticspider.parseHtml()
    staticspider.getHrefs()
    staticspider.getFormurls()
    
    surls = staticspider.getUrls()
    
    for d in surls:
        print(d)
    print("##############################")   
    print("############动态爬虫#############")
    dynamicspider = DynamicSpider.DynamicSpider()
    dynamicspider.setUrl(url)
    dynamicspider.loadAsynHtml()
    dynamicspider.getClickButtonsurls()
    durls = dynamicspider.getUrls()
    
    for d in durls:
        print(d) 
        
    print("#############END##################")
    

def test2():
    url = "http://127.0.0.1:8080/web/index.html"
    spider = SpiderOperation.SpiderOperation()
    spider.init(2, url)
    spider.startSpider()
    rurls = spider.getUrls()
    print("spider results:")
    for u in rurls.keys():
        print("%s %s" % (u,rurls[u]))
    fileop = FileOperation.FileOperaton()
    fileop.fileWrite(rurls)
    
    fr = fileop.fileRead()
    for u in fr.keys():
        print("%s %s" % (u,fr[u]))
    print(("##############END#################"))
if __name__ == "__main__":
    
    test2()
    
#     domscanner = DomxssScanner.DomxssScanner()
#     payloads = []
#     
#     a = "{\"poc\":\"<script>alert(0);</script>\",\"check\":\"console\"}"
#     b = "{\"poc\":\"<script>alert(0);</script>\",\"check\":\"tag\"}"
#     payloads.append(a)
#     payloads.append(b)
#     url = {'id': 2, 'method': 'GET', 'url': 'http://127.0.0.1:8009/webtest/?default=hello&abc=a', 'postdata': ''}
#     domscanner.setUrl("http://127.0.0.1:8009/webtest/?default=%3Cscript%3Econsole.log(1234);%3C/script%3E")
#     domscanner.setPayloads(payloads)
#     domscanner.dealUrl(url)
#     domscanner.scanUrl(payloads)