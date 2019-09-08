# -*- coding: UTF-8 -*-

'''
通过burpsuite拦截获取报文，将请求保存至raw.request文件中，输出对应的json格式header、cookies、parameters
'''
import json
from numpy.core.defchararray import rindex

class reqTojson:
    def __init__(self):
        self.filename = r'raw.request'
        #需要输出的数据，包含域名、请求头、cookies、参数
        self.domain = ''
        self.headers = {}
        self.cookies = {}
        self.params = {}
        self.method = ''
        #该flag标识，判断是否为空白行，如果是，则下面的为post参数
        self.isblank = False

    def openraw(self):
        self.fin = open(self.filename,'r')
        return self.fin
    
    '''
    读取内容，处理内容
    '''
    def parserawreq(self):
        while True:
            linecon = self.fin.readline()
            if not linecon:
                break
            linecon = linecon.rstrip('\r\n')
            linecon =linecon.strip(' ')
            if linecon.find('GET')==0 or linecon.find('POST')==0:      #处理URI，获取URI以及参数
                index = linecon.find(' ')
                self.method = linecon[0:index]
                linecon =linecon[index+1:]
                index = linecon.find(' ')
                linecon = linecon[0:index]
                index = linecon.find('?')
                self.domain = linecon[0:index]
                linecon = linecon[index+1:]
                if(linecon == ' '):
                    continue
                para = []
                while linecon.find('&') != -1:
                    index = linecon.find('&')
                    para.append(linecon[0:index])
                    linecon = linecon[index+1:]
                para.append(linecon)
                for el in para:
                    if el.find('=') != -1:
                        index = el.find('=')
                        self.params[el[0:index]] = el[index+1:]
            elif linecon.find('Host:') == 0:                       #处理域名
                index = linecon.find(":")
                linecon = linecon[index+1:].strip(' ')
                self.domain =  linecon + self.domain

            elif linecon.find('Cookie:') == 0:
                index = linecon.find(":")
                linecon = linecon[index+1:].strip(' ')
                para = []
                while linecon.find(';') != -1:
                    ndex = linecon.find(';')
                    para.append(linecon[0:index])
                    linecon = linecon[index+1:].strip(' ')
                para.append(linecon)     
                for el in para:
                    if el.find('=') != -1:
                        index = el.find('=')
                        self.cookies[el[0:index]] = el[index+1:]
            #判断是否为空白行 
            elif len(linecon)==0:
                self.isblank = True
            
            elif not self.isblank:         #处理headers
                index = linecon.find(":")
                self.headers[linecon[0:index]] = linecon[index+1:].strip(' ')
    
            elif self.isblank:            #处理POST请求参数 
                if(linecon == ' '):
                    continue
                para = []
                #如果是json格式
                linecon = linecon.strip()
                if linecon.find("{") == 0:
                    linecon = json.loads(linecon)
                    for key in linecon.keys():
                        self.params[key] = linecon[key]
                    break;
                #处理普通参数类型
                while linecon.find('&') != -1:
                    index = linecon.find('&')
                    para.append(linecon[0:index])
                    linecon = linecon[index+1:]
                    para.append(linecon)
        
                for el in para:
                    if el.find('=') != -1:
                        index = el.find('=')
                        self.params[el[0:index]] = el[index+1:]
                
        
    def getdomain(self):
        print('Url:\r    '+self.domain)
        return self.domain
    def getheaders(self):
        print('Headers:\r    %s' % (self.headers))
        return self.headers
    def getcookies(self):
        print('Cookies:\r    %s' % (self.cookies))
        return self.cookies
    def getparams(self):
        print('params:\r    %s' % (self.params))
        return self.params
    
if __name__ == '__main__':
    req = reqTojson()
    req.openraw()
    req.parserawreq()
    req.getdomain()
    req.getheaders()
    req.getcookies()
    req.getparams()
    
        