#!/usr/bin/python

from urllib.parse import urlparse
from urllib.parse import parse_qs
from tools import FileOperation
from scanner.DomxssScanner import DomxssScanner
from asyncio.tasks import sleep
import json


class ScanOperation:
    
    def  __init__(self):
        self.lasttimes = 0
        self.urlsnumber = 0
        self.payloadnumber = 0
        self.paramsnumbers = 0
        self.seconds = 0
        print("init")
    '''
    打印扫描剩余时间
    没一条待扫描URL耗时: 1*(poc数量)*参数数量*10秒
    '''
    def printReqtime(self):
        self.payloadnumber = len(self.payloads)
        self.urlsnumber = len(self.urls)
        
        for d in self.urls.keys():
            url = json.loads(self.urls[d])
            url_parse = urlparse(url['url'])   
            url_params = parse_qs(url_parse.query)
            url_postdata = parse_qs(url['postdata'])
            self.paramsnumbers = self.paramsnumbers + len(url_params) + len(url_postdata)
        
        self.seconds = self.payloadnumber * self.paramsnumbers * 10
        m, s = divmod(self.seconds, 60)
        h, m = divmod(m, 60)
        print ("本次扫描预计耗时：:    %02d:%02d:%02d" % (h, m, s))
    
    '''
    更新时间,扫描完一条URL则减少该URL（参数*10）的耗时
    '''
    def updateReqtime(self,url):
        url = json.loads(url)
        url_parse = urlparse(url['url'])   
        url_params = parse_qs(url_parse.query)
        url_postdata = parse_qs(url['postdata'])
        usetime = (len(url_params) + len(url_postdata))*10*len(self.payloads)
        self.seconds = self.seconds - usetime
        m, s = divmod(self.seconds, 60)
        h, m = divmod(m, 60)
        print ("本次扫描剩余耗时：:    %02d:%02d:%02d" % (h, m, s))
    
    def loadUrls(self):
        urls = FileOperation.FileOperaton().fileRead()
        self.urls = urls
        return urls
    
    def loadPayloads(self):
        payloads = FileOperation.FileOperaton().loadPayloads()
        self.payloads = payloads
        return payloads
    
    def startScan(self):
        self.loadPayloads()
        self.loadUrls()
        self.printReqtime()
        
        #开始扫描
        for url in self.urls.keys():
            print("正在扫描：%s" % (self.urls[url]))
#             self.scanOneurls(self.urls[url])
            self.updateReqtime(self.urls[url])
    
    '''
    扫描单个URL
    '''    
    def scanOneurls(self,url):
        
        dscanner = DomxssScanner()
        dscanner.setPayloads(self.payloads)
        dscanner.dealUrl(url)        
        dscanner.end()
        
                
#         self.payloads = payloads
#         self.
#         for url in urls.keys():
#             print(urls[url])
#             dscanner = DomxssScanner()
#             dscanner.__init__()
#             dscanner.setPayloads(payloads)
#             dscanner.dealUrl(urls[url])