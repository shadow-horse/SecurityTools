#!/usr/bin/python

"""爬虫：爬取Href属性的链接"""
import requests
import json
from bs4 import BeautifulSoup
from _socket import timeout
from spider.DynamicSpider import DynamicSpider
class HrefSpider:
    '''
    初始化参数
    '''
    def setUrl(self,url):
        self.url = url;
        self.list = []
    '''
    此函数用于获取网页的内容
    '''
    def getHtmlText(self):
        try:
            res = requests.get(self.url,timeout = 6)
            #判断是否HttpError
            res.raise_for_status()
            res.encoding = res.apparent_encoding
            self.htmltext = res.text
            #解析html代码
            self.soup = BeautifulSoup(self.htmltext,'html.parser')
            return res.text
        except:
            print("getHtmlText 产生异常")
    '''
    获取href属性链接
    '''
    def getHrefs(self):
        #模糊搜索获取HTML代码所有<a href="">属性值
        self.hreflist = []
        a_hrefs = self.soup.find_all('a', attrs={'href':True})
        for a in a_hrefs:
            self.hreflist.append(a.get('href'))
        return self.hreflist
    '''
    获取src属性链接
    '''
    def getSrc(self):
        a_srcs = self.soup.find_all('*', attrs={'src':True})
        return a_srcs
    
    '''
    传入网页内容，进行解析
    '''
    def setHtmltext(self,text):
        self.htmltext = text
        self.soup = BeautifulSoup(self.htmltext,'html.parser')
    
    
if __name__ == "__main__":
    spider = HrefSpider();
    spider.setUrl("https://weibo.com/")
    spider.getHtmlText()
    result = spider.getHrefs()
    for a in result:
        print(a)
    print("================================")
    
    dspider = DynamicSpider();
    dspider.setUrl("https://weibo.com/")
    dspider.loadAsynHtml()
    restext = dspider.getHtmltext()
    spider.setHtmltext(restext)
    result = spider.getHrefs()
    for a in result:
        print(a)
    print("================================")
    
    result = dspider.getRequestlists()
    for data in result:
        print(data)
    
