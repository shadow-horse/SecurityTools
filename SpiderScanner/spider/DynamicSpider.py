#!/usr/bin/python

import time
import json
import warnings
from selenium import webdriver
from bs4 import BeautifulSoup


"""
动态抓取网页内容
"""
class DynamicSpider:
    def __init__(self):
        warnings.filterwarnings("ignore")
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
        self.reqlists = []
        self.cookies = []

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
        
        self.browser.add_cookie(cookie)
                    
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
        #获取browser log内容，我们将获取到的信息写入了browser log，目前不知道是否还有其它获取内容的API接口,通过filter进行过去
        self.requestlists = filter(lambda x:'url' in x,self.browser.get_log('browser'))
        #添加保存链接
        self.addRequestlists(self.requestlists)
        
    def getHtmltext(self):
        return self.pagesource
    
    '''
    添加request list，处理数据格式，获取有效的请求
    '''
    def addRequestlists(self,lists):
        
        id = 1
        for req in lists:
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
    '''
    获取爬取的链接
    '''
    def getUrls(self):
        return self.reqlists
    '''
    解析触发事件，获取发起的响应
    '''
    def getClickButtonsurls(self):
#         print("###################################")
        self.button_requests = []
        htmltext = self.browser.page_source
        self.soup = BeautifulSoup(htmltext,'html.parser')
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
                #不需要等待，直接获取发出的请求
                submit_reqs = filter(lambda x: 'url' in x, self.browser.get_log('browser'))
                self.addRequestlists(submit_reqs)
#                 print(submit_reqs)
                #重写页面内容，返回上一页内容,EOF报错暂时无法解决
                #redojs = "document.body.innerHTML='';document.write('"+htmltext+"');"
                #self.browser.execute_script(redojs)
                # 重新加载页面，耗费时间，及时重新加载如果超时或页面变动，可能导致DOM结构变化
                self.browser.get(self.url)  
                time.sleep(10) #直接设置等待10s
                self.requestlists = filter(lambda x: 'url' in x, self.browser.get_log('browser'))
                # 可以选择忽略，但是如果click请求发生跳转，会导致页面发生变化，无法继续处理当前的页面
                
                #删除node节点，删除已经被执行过的submit
                deljs = self.delNode('input', 'type', 'submit')
                self.browser.execute_script(deljs)
            except:
                break
        #循环遍历input button
        for input in input_button:
            try:
                # 在执行Click之前保存页面
                htmltext = self.browser.page_source
                # driver通过xpath查询，点击触发第一个submit
                self.browser.find_element_by_xpath("//input[@type='button']").click()
                #不需要等待，直接获取发出的请求
                submit_reqs = filter(lambda x: 'url' in x, self.browser.get_log('browser'))
                self.addRequestlists(submit_reqs)
#                 print(submit_reqs)
                #重写页面内容，返回上一页内容,EOF报错暂时无法解决
                #redojs = "document.body.innerHTML='';document.write('"+htmltext+"');"
                #self.browser.execute_script(redojs)
                # 重新加载页面，耗费时间，及时重新加载如果超时或页面变动，可能导致DOM结构变化
                self.browser.get(self.url)  
                time.sleep(10) #直接设置等待10s
                self.requestlists = filter(lambda x: 'url' in x, self.browser.get_log('browser'))
                # 可以选择忽略，但是如果click请求发生跳转，会导致页面发生变化，无法继续处理当前的页面
            
                #删除node节点，删除已经被执行过的submit
                deljs = self.delNode('input', 'type', 'button')
                self.browser.execute_script(deljs)
            except:
                break
        
        #buttons
        for input in buttons:
            try:
                # 在执行Click之前保存页面
                htmltext = self.browser.page_source
                # driver通过xpath查询，点击触发第一个submit
                self.browser.find_element_by_xpath("//button").click()
                #不需要等待，直接获取发出的请求
                submit_reqs = filter(lambda x: 'url' in x, self.browser.get_log('browser'))
                self.addRequestlists(submit_reqs)
#                 print(submit_reqs)
                #重写页面内容，返回上一页内容,EOF报错暂时无法解决
                #redojs = "document.body.innerHTML='';document.write('"+htmltext+"');"
                #self.browser.execute_script(redojs)
                # 重新加载页面，耗费时间，及时重新加载如果超时或页面变动，可能导致DOM结构变化
                self.browser.get(self.url)  
                time.sleep(10) #直接设置等待10s
                self.requestlists = filter(lambda x: 'url' in x, self.browser.get_log('browser'))
                # 可以选择忽略，但是如果click请求发生跳转，会导致页面发生变化，无法继续处理当前的页面
            
                #删除node节点，删除已经被执行过的submit
                deljs = self.delNode('button', '', '')
                self.browser.execute_script(deljs)
            except:
                break
    
    '''
    利用上述接口的方式可以触发所有onxxx事件的请求，目前没有找好直接通过属性获取Tag的方式，需要遍历相关标签的ON事件
    例如<a href="javascript:0" onclick="" />
    '''  
    def getOnxxxurls(self):
        return ""
          
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
