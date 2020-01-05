#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名称: socketClient.py
# author: snowsec0

import socket
from asyncio.tasks import sleep

class socketClient():
    
    def __init__(self):
        self.filename = ''
        self.host = ''
        self.port = 0
        self.msg = ''
    
    def sethost(self,host):
        self.host = host
    
    def setport(self,port):
        self.port = port    
    
    def sendmsg(self,msg):
        if(msg == None):
            self.msg = ''
        else:
            self.msg = msg
        try:
            s = socket.socket()
            s.settimeout(10)
            s.connect((self.host,self.port))
            s.send(self.msg.encode('utf-8'))
            self.backinfo = s.recv(2048)
            s.close()
            return self.backinfo
        except Exception as e:
            print('[socketclient][sendmsg][exception] %s,%d'%(self.host,self.port))
            return 'exception'
        
    def sendfileinfo(self,host,port,filename):
        self.host = host
        self.port = port
        self.filename = filename
        if(not self.checkparams()):
            return 'error'
        if (not self.readfilemsg()):
            return 'exception'
        try:
            s = socket.socket()
            s.settimeout(10)
            s.connect((host,port))
            s.send(self.filemsg)
            self.backinfo = s.recv(2018)
            s.close()
            return self.backinfo
        
        except Exception as e :
            print('[socketclient][sendfileinfo][exception] %s,%d'%(self.host,self.port))
            return 'exception'
            
    #检查参数
    def checkparams(self):
        if self.host == '' or self.port == 0 :
            print('[socketclient][checkparams][error] %s,%d'%(self.host,self.port))
            return False
        else:
            return True
    
    #读取文件二进制内容
    def readfilemsg(self):
        try:
            fo = open (self.filename,'rb')
            content = fo.read()
            self.filemsg = content
            fo.close()
            return True
        except Exception as e:
            print('[socketclient][readfilemsg][exception] %s'%(self.filename))
            return False

if __name__ == '__main__':
    socketclient = socketClient()
    