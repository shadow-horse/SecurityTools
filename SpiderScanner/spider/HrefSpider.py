#!/usr/bin/python

"""爬虫：爬取Href属性的链接"""
import requests
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from _socket import timeout
from spider.DynamicSpider import DynamicSpider
from tools import Deldump

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
        
        self.hreflist = self.formatGetUrl(self.fillUrls(self.hreflist))                    
        return self.hreflist
    '''
    获取静态form表单请求
    '''
    def getFormurls(self):
        self.formlist = []
        form_res = self.soup.find_all("form")
        # 遍历form表单
        i = 1
        for one_f in form_res:
            attrs = one_f.attrs
            form_value = {}
            form_value['id'] = i
            form_value['method'] = 'GET'
            form_value['url'] = ''
            form_value['postdata'] = ''
            
            if 'action' in attrs:
                form_value['url'] = self.fillUrl(one_f['action'])
            if 'method' in attrs:
                form_value['method'] = one_f['method']
            #获取input组件参数    
            input_one = one_f.find_all("input",attrs={'name':True})
            params = ""
            for one_i in input_one:
                if('type' in one_i.attrs):
                    if (one_i['type'] == 'submit'):
                        continue;
                params = params + one_i['name'] +'=20%&'
            form_value['postdata'] = params
            if(form_value['url'] != ''):
                self.formlist.append(form_value)  
                i = i + 1
        return self.formlist
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
    
    '''
    处理拼接返回完整的URL
    '''
    def fillUrls(self,lists):
        #简单补齐域名
        hlist = []
        for l in lists:
            l = self.fillUrl(l)    
            if(l.startswith("javascript:")):
                continue
            hlist.append(l)
        return hlist
    def fillUrl(self,url):
        host_urlparse = urlparse(self.url)
        l = url.strip()
        if(l.startswith("//")):  # ”//“开头，直接访问域名
            l = host_urlparse.scheme+":"+l
        elif(l.startswith("/")): # ”/“开头，是从当前域名的根目录进行访问
            l = host_urlparse.scheme+"://"+host_urlparse.netloc+l
        elif(l.startswith("javascript:")):
            return 'javascript:'
        elif not(l.startswith("https://") or l.startswith("http://")):
            #如果不是http、https、javascript伪协议，则默认设置为从当前路径访问（存在其它协议过滤不全的问题，如ftp://,此处暂不考虑）
            if(host_urlparse.path == ''):
                l = host_urlparse.scheme + "://" +host_urlparse.netloc + '/' + l
            else:
                l = host_urlparse.scheme + "://" +host_urlparse.netloc + host_urlparse.path + l
        return l
    '''
    格式化爬起的URL
    '''
    def formatGetUrl(self,lists):
        #href,src链接基本都是GET请求
        urlinfo = []
        i = 1
        for l in lists:
            oneurl = {}
            oneurl['id'] = i
            oneurl['method'] = 'GET'
            oneurl['url'] = l
            oneurl['postdata'] = ''
            urlinfo.append(oneurl)
            i = i+1
        return urlinfo
        
if __name__ == "__main__":
    #静态页面访问
    spider = HrefSpider();
    spider.setUrl("http://127.0.0.1/xss/domxss.html")
    spider.getHtmlText()
    result = spider.getHrefs()
    for a in result:
        print(a)
    print("================================")
    #等待动态Ajax加载，获取发出的请求
    dspider = DynamicSpider();
    dspider.setUrl("http://127.0.0.1/xss/domxss.html")
    dspider.loadAsynHtml()
    dreqlist = dspider.getRequestlists()
    
    #页面加载完成后，静态解析页面，爬取链接
    restext = dspider.getHtmltext()
    spider.setHtmltext(restext)
    dhreflist = spider.getHrefs()
    dformlist = spider.getFormurls()
    print("================================")
    
    #合并两部分内容
    reqlist = []
    for a in dhreflist:
        reqlist.append(a)
    for a in dreqlist:
        reqlist.append(a)   
    for a in dformlist:
        reqlist.append(a) 
        
    delDump = Deldump.Deldump()
    result = delDump.deldumpurls(reqlist)
    for data in result.keys():
        print("%s : %s" % (data,result[data]))
    print('execute end.')
