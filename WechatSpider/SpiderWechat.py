#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from urllib.parse import urlparse, urlencode
from bs4 import BeautifulSoup
import urllib3
from HttpTools import HttpTools
from urllib import parse
from asyncio.tasks import sleep

'''
说明：
    利用搜狗的wechat查询接口查询微信公众号，但是获取到的微信公众号，只能查看十条数据
'''
#设置重连次数
requests.adapters.DEFAULT_RETRIES = 5  
#屏蔽ssl的告警
urllib3.disable_warnings()


class SpiderWechat:
    
    def __init__(self):
        self.sogou = "https://weixin.sogou.com/weixin?type=1&ie=utf8&s_from=input&_sug_=n&_sug_type_=&query="
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
                        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                        'Accept-Encoding':'gzip, deflate',
                        'Referer':'https://weixin.sogou.com/',
                        'Connection':'close',
                        'Upgrade-Insecure-Requests':'1'
                        }
        
        self.cookies = {}
        self.domain = ".sogou.com"
        
    def setWecPubNum(self,wechatpubnum):
        self.wechatpubnum = wechatpubnum
        self.sogou = self.sogou + parse.quote_plus(self.wechatpubnum)
        print(self.sogou)
        
    
    def queryBysougou(self):
        httpTools = HttpTools(self.sogou,domain=self.domain,cookies=self.cookies,headers=self.headers)
        #优先采用静态获取响应，在爬取时需要注意爬取的速率，否则容易弹出验证码
#         httpTools.initdynamic()
#         res = httpTools.dynamicGetRequest()
        self.res = httpTools.getRequest()
        return self.res
        
    '''
    说明：
        解析响应，获取查询到的第一条记录，返回链接地址
    '''
    def getWechaturl(self):
        self.res = ""
        print("文件操作")
        fo = open("response.txt")
        for line in fo.readlines():
            self.res = self.res + line
        soup = BeautifulSoup(self.res,'lxml')
        a_tags = soup.findAll('a')
        for item  in a_tags:
            print(item)
        
        return ""
print("=========start===========")
spiderWechat = SpiderWechat()
spiderWechat.setWecPubNum('月色下')
# spiderWechat.queryBysougou()
spiderWechat.getWechaturl()
print("=========end=============")