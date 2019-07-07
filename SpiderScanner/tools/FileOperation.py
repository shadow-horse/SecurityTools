#!/usr/bin/python
import json

#文件异常未处理
class FileOperaton:
    
    #保存爬取的链接，暂时不考虑写过程的去重
    def fileWrite(self,data,filename="spider.urls.txt"):
        fo = open(filename,"w+")
        for line in data.keys():
            fo.write(line +":"+json.dumps(data[line])+"\n")
        
        fo.close()
    
    #读取爬虫文件，返回链接对象
    def fileRead(self,filename="spider.urls.txt"):
        fo = open(filename,'r')
        urllists = {}
        for line in fo.readlines():
            index = line.index(":")
            key = line[:index]
            value = line[index:]
            urllists[key]=value
        fo.close()
        return urllists
    
    #读取payload文件，返回poc
    '''
    {"poc":"<script>console.log('12345678');</script>","type":"console","verify":"12345678"}
    poc: 发送的攻击payload
    type: 检测响应的方式
    verify: 检测的字符串或关键代码
    '''
    def loadPayloads(self,filename="payloads.txt"):
        fo = open(filename)
        payloads = []
        for line in fo.readlines():
            payloads.append(line)
            print(payloads)
            return payloads