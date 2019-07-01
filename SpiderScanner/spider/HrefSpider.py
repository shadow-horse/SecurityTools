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
    def getHtmlText(self,url):
        try:
            res = requests.get(url,timeout = 6)
            #判断是否HttpError
            res.raise_for_status()
            res.encoding = res.apparent_encoding
            return res.text
        except:
            print("getHtmlText 产生异常")
    '''
    此函数用于解析获取href属性值
    '''    
    def parseHtmlText(self,text):
        #解析html代码
        soup = BeautifulSoup(text,'html.parser')
        #模糊搜索获取HTML代码所有<a href="">属性值
        a_hrefs = soup.find_all('a', attrs={'href':True})
        return a_hrefs
    
    def getHrefs(self):
        text = self.getHtmlText(self.url)
        a_hrefs = self.parseHtmlText(text)
        
        for a in a_hrefs:
            self.list.append(a.get('href'))
        return self.list
    
if __name__ == "__main__":
#     spider = HrefSpider();
#     spider.setUrl("https://weibo.com/")
#     result = spider.getHrefs()
#     for a in result:
#         print(a)
    print("================================")
    dspider = DynamicSpider();
    dspider.setUrl("https://weibo.com/")
    dspider.loadAsynHtml()
    result = dspider.getRequestlists()
    for data in result:
        print(data)
    
