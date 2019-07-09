#!/usr/bin/python

import time
import json
import copy
import warnings
import requests
import urllib.parse
from selenium import webdriver
from urllib.parse import urlparse
from urllib.parse import parse_qs
from asyncio.tasks import sleep
from bs4 import BeautifulSoup
from tools import FileOperation

"""
DOM XSS扫描
问题：
     基于一条URL扫描所有的payloads，当扫描发现某个参数时，未及时终止（很浪费时间，设置全局变量，break）
"""
class DomxssScanner:
    def __init__(self):
        warnings.filterwarnings("ignore")
        self.service_args = []
        self.service_args.append('--load-images=no')  #关闭图片加载
        self.service_args.append('--disk-cache=yes')  #开启缓存
        self.service_args.append('--ignore-ssl-errors=true') #忽略证书错误
        self.browser = webdriver.PhantomJS("/Users/snow/programs/phantomjs-2.1.1-macosx/bin/phantomjs",service_args=self.service_args)
        #explicit waits 和implicit wait 在获取element前，等待Ajax执行完毕
        self.browser.implicitly_wait(10)
        self.logs = []
        self.pages = []
        
    def end(self):
        self.browser.close()    
    '''
    初始化
    '''
    def setUrl(self,url):
        self.url = url
        self.cookies = []
        self.logs = []
        self.pages = []
    
    def setCookies(self,domain,name,value):
        #清除Cookie
        self.browser.get(self.url) 
        self.browser.delete_all_cookies()
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
        self.cookies.append(cookie)
        self.browser.add_cookie(cookie)
    '''
    GET方式扫描URL
    '''
    def scanGeturl(self,payload,newurl):
        script = "var page = this; page.onConsoleMessage = function(msg) {page.browserLog.push(msg);};"
        self.browser.command_executor._commands['executePhantomScript'] = ('POST', '/session/$sessionId/phantom/execute')
        self.browser.execute('executePhantomScript', {'script': script, 'args': []})
        #检测前抽取参数
        self.browser.get(newurl)  
        time.sleep(3) #直接设置等待10s
        
        pagesource = self.browser.page_source 
        self.addPagecontent(self.browser.page_source)
        logs = self.browser.get_log('browser')
        self.addLog(logs)
        self.checkClickButtons(payload,newurl)
        #检测POC
        self.checkPayloads(payload, self.pages, self.logs, newurl)
#         print(self.pagesource)
    '''
    POST方式扫描URL
    '''
    def scanPosturl(self,payload,newurl,data):
        
        #输出日志
        script = "var page = this; page.onConsoleMessage = function(msg) {page.browserLog.push(msg);};"
        self.browser.command_executor._commands['executePhantomScript'] = ('POST', '/session/$sessionId/phantom/execute')
        self.browser.execute('executePhantomScript', {'script': script, 'args': []})
        #发起GET请求，设置同域，最好的链接应该是POST请求的母链接
        self.browser.get(newurl)  
        sleep(1)
        winhandlers = self.browser.window_handles
        befhandler = winhandlers[0]
        #加载执行jquery.js
        jquery = open("jquery-3.4.1.min.js", "r").read() 
        self.browser.execute_script(jquery)
        #构造POST请求，打开新的标签页面
        request_type="'POST'"
        ajax_query = '''
            $.ajax('%s', {
            type: %s,
            data: %s, 
            headers: { "User-Agent": "Mozilla/5.0" },
            crossDomain: true,
            xhrFields: {
             withCredentials: true
            },
            success: function(str_response){var obj = window.open("about:blank");   
                        obj.document.write(str_response);   }
            });
            ''' % (newurl, request_type, data)
            
        ajax_query = ajax_query.replace("\n", "")


        resp = self.browser.execute_script("return " + ajax_query)
        time.sleep(2)
        newhandler = ""
        winhandlers = self.browser.window_handles
        for a in winhandlers:
            if(a != befhandler):
                newhandler = a 
        #切换至新的标签页（理论上仅有2个）
        self.browser.switch_to.window(newhandler)
        logs = self.browser.get_log('browser')
        log = []
        for l in logs:
            ldata = l['message'] 
            ldata = ldata[:ldata.rfind(" (:)")]
            log.append(ldata)
        self.addLog(log)
        self.addPagecontent(self.browser.page_source)
        
        self.addPagecontent(resp)
        self.checkPayloads(payload, self.pages,logs, newurl+json.dumps(data))
        #JS执行页面未变换，失败
    '''
    静态扫描POST请求，selenium发起post请求未验证是否能加载到当前页面
    加载payload异常
    '''    
    def scanStaicposturl(self,payload,newurl,data):
        try:
            res = requests.post(url=newurl,data=data,headers={'Content-Type':'application/x-www-form-urlencoded'})
            #判断是否HttpError
            res.raise_for_status()
            res.encoding = res.apparent_encoding
            self.addPagecontent(res.text)
            #POST请求暂时不处理logs事件，只检测DOM节点变化
            logs = []
            self.checkPayloads(payload, self.pages,logs, newurl)
        except:
            print("scanStaicposturl 产生异常")
    
    '''
    Javascript发起Ajax请求
    '''    
    def postjs(self,url,data):
        js = "var xmlhttp=new XMLHttpRequest();";
        js = js +"xmlhttp.open(\"POST\",\"" + url +"\",false);";
        js = js + "xmlhttp.setRequestHeader(\"Content-type\",\"application/x-www-form-urlencoded\");";
        js = js + "xmlhttp.setRequestHeader(\"User-Agent\",\"Mozilla/5.0\");";
        js = js + "xmlhttp.setRequestHeader(\"Cookie\",\"\");";
        #POST请求暂时不支持设置Cookie  xmlhttp.setRequestHeader("Cookie",""); 
        datastr = urllib.parse.urlencode(data)
#         for d in data.keys():
#             datastr = datastr + d + "=" + urllib.parse.urlencode(data[d]) + "&"
        js = js + "xmlhttp.send(\"" +datastr+"\");";
        js = js + "return xmlhttp.responseText;";
        return js
    
    def dealUrl(self,url):
        #GET请求参数处理
        self.url = json.loads(url)
        url_parse = urlparse(self.url['url'])
        url_params = parse_qs(url_parse.query)
        url_postdata = parse_qs(self.url['postdata'])
        domain = url_parse.scheme + "://" + url_parse.netloc + url_parse.path
        
        #循环拼接参数，处理GET请求
        if(self.url['method'] == 'GET' or self.url['method'] == 'get'):
            for p in url_postdata.keys():
                url_params[p] = url_postdata[p]
            #如果是GET请求，则清空post数据
            url_postdata = []
        
            #针对每一个参数，循环遍历payloads
            for param in url_params:
                temp_params = copy.deepcopy(url_params)
                for payload in self.payloads:
                    self.logs = []
                    self.pages = []
                    payload = json.loads(payload)
                    temp_params[param][0] = payload["poc"]
                    newurl = self.spliceurl(domain,temp_params)
                    #扫描请求
                    print("正在扫描: "+newurl)
                    self.scanGeturl(payload,newurl)
        #处理POST请求
        if(self.url['method'] == 'POST' or self.url['method'] == 'post'):
            postdata = {}
            url = self.url['url']
            
            for key in url_postdata.keys():
                postdata = copy.deepcopy(url_postdata)
                for d in postdata.keys():
                    postdata[d] = postdata[d][0]
                for payload in self.payloads:
                    self.logs = []
                    self.pages = []
                    payload = json.loads(payload)
                    postdata[key] = payload["poc"]
                    print("正在扫描: %s:%s:%s" % (url,key,payload["poc"]))
#                     self.scanStaicposturl(payload, url, postdata)
                    self.scanPosturl(payload, url, postdata)
                
            
    def spliceurl(self,domain,params):
        url = domain
        url = url + "?"
        for p in params.keys():
            url = url + p + "=" + params[p][0] +"&"
        return url
    
    def setPayloads(self,payloads):     
        self.payloads = payloads
        
    '''
    检测payload
    '''
    def checkPayloads(self,payload,pagesources,logs,url):
        #检测到存在漏洞需要停止该参数的扫描，但是目前的实现逻辑，是扫描完后判断是否存在注入
        if(payload['type'] == 'console'):#如果type=console，则检测logs
            checkdata = payload['verify']
            for log in logs:
                if(checkdata == log):
                    file = FileOperation.FileOperaton()
                    file.writeDomxssurl(url,payload)
                    print("【domxss】%s:%s" % (url,payload))
                    break
        #检测dom节点变化
        if(payload['type'] == 'domtag'):
            domtag = payload['verify']
            for pagesource in pagesources:
                try:
                    parse = BeautifulSoup(pagesource,'html.parser')
                    domtags = parse.find_all(domtag)
                    if len(domtags) > 0:
                        file = FileOperation.FileOperaton()
                        file.writeDomxssurl(url,payload)
                        print("【domxss】%s:%s" % (url,payload))
                        break
                except:
                    print("【error】html parse解析失败")
                    continue    
        if(payload['type'] == 'textplain'):
            checkplain = payload['verify']
            for pagesource in pagesources:
                if pagesource.find(checkplain) != -1 :
                    file = FileOperation.FileOperaton()
                    file.writeDomxssurl(url,payload)
                    print("【domxss】%s:%s" % (url,payload))
                    break
                    
            
#         elif(payload['type'] == 'domtag'):#如果type=domtag，则检测pagesource
        
    '''
    解析触发事件，获取发起的响应
    '''
    def checkClickButtons(self,payload,newurl):
#         print("###################################")
        htmltext = self.browser.page_source
        try:
            self.soup = BeautifulSoup(htmltext,'html.parser')
        except:
            print("【error】html parser failed: " + newurl)
            return
        # input button 
        input_button = self.soup.find_all('input', attrs={'type':'button'})
        input_submit = self.soup.find_all('input', attrs={'type':'submit'})
        buttons = self.soup.find_all('button')
        
        # 循环遍历触发input submit事件
        for input in input_submit:
            try:
                # 在执行Click之前保存页面
                htmltext = self.browser.page_source
                # driver通过xpath查询，点击触发第一个submit
                self.browser.find_element_by_xpath("//input[@type='submit']").click()
                sleep(1)
                self.addPagecontent(self.browser.page_source)
                submit_reqs = self.browser.get_log('browser')
                self.addLog(submit_reqs)
                self.browser.get(newurl)  
                time.sleep(3) #直接设置等待10s
                self.requestlists = self.browser.get_log('browser')
                # 可以选择忽略，但是如果click请求发生跳转，会导致页面发生变化，无法继续处理当前的页面
                
                #删除node节点，删除已经被执行过的submit
                deljs = self.delNode('input', 'type', 'submit')
                self.browser.execute_script(deljs)
            except:
                print("exception input submit")
                break
        #循环遍历input button
        for input in input_button:
            try:
                # 在执行Click之前保存页面
                htmltext = self.browser.page_source
                # driver通过xpath查询，点击触发第一个submit
                self.browser.find_element_by_xpath("//input[@type='button']").click()
                sleep(1)
                self.addPagecontent(self.browser.page_source)
                submit_reqs =  self.browser.get_log('browser')
                self.addRequestlists(submit_reqs)
                # 重新加载页面，耗费时间，及时重新加载如果超时或页面变动，可能导致DOM结构变化
                self.browser.get(newurl)  
                time.sleep(3) #直接设置等待10s
                self.requestlists = self.browser.get_log('browser')
                # 可以选择忽略，但是如果click请求发生跳转，会导致页面发生变化，无法继续处理当前的页面
            
                #删除node节点，删除已经被执行过的submit
                deljs = self.delNode('input', 'type', 'button')
                self.browser.execute_script(deljs)
            except:
                print("exception input button")
                break
        
        #buttons
        for input in buttons:
            try:
                # 在执行Click之前保存页面
                htmltext = self.browser.page_source
                # driver通过xpath查询，点击触发第一个submit
                self.browser.find_element_by_xpath("//button").click()
                sleep(1)
                self.addPagecontent(self.browser.page_source)
                submit_reqs = self.browser.get_log('browser')
                self.addLog(submit_reqs)
                # 重新加载页面，耗费时间，及时重新加载如果超时或页面变动，可能导致DOM结构变化
                self.browser.get(newurl)  
                time.sleep(3) #直接设置等待10s
                self.requestlists =  self.browser.get_log('browser')
                # 可以选择忽略，但是如果click请求发生跳转，会导致页面发生变化，无法继续处理当前的页面
            
                #删除node节点，删除已经被执行过的submit
                deljs = self.delNode('button', '', '')
                self.browser.execute_script(deljs)
            except:
                print("exception buttons")
                break
    '''
    执行JS删除node节点
    '''
    def delNode(self,tagname,type,value):
        if(type == ''):
            jscode ="var deleteNode =document.getElementsByTagName('" +tagname+"');for (var i=0 ; i<deleteNode.length;i++){var node = deleteNode[i];node.parentNode.removeChild(node); }"
        else:
            jscode ="var deleteNode =document.getElementsByTagName('" +tagname+"');for (var i=0 ; i<deleteNode.length;i++){var node = deleteNode[i];var value = node.getAttribute('"+type+"');if(value == '"+value+"'){node.parentNode.removeChild(node);break;} }"
        return jscode
    
        return ""    

    '''
    汇总所有的logs
    '''  
    def addLog(self,logs):
        for log in logs:
            self.logs.append(log)
    '''
    汇总所有页面
    '''
    def addPagecontent(self,pagesource):
        self.pages.append(pagesource)