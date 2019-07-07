#!/usr/bin/python

from spider import StaticSpider
from spider import DynamicSpider
from scanner import DomxssScanner
from tools import Deldump
from tools import FileOperation

if __name__ == "__main__":
    
    print("begin")
    
    url = ""
    
    domscanner = DomxssScanner.DomxssScanner()
    payloads = []
    
    a = "{\"poc\":\"<script>alert(0);</script>\",\"check\":\"console\"}"
    b = "{\"poc\":\"<script>alert(0);</script>\",\"check\":\"tag\"}"
    payloads.append(a)
    payloads.append(b)
    url = {'id': 2, 'method': 'GET', 'url': 'http://127.0.0.1:8009/webtest/?default=hello&abc=a', 'postdata': ''}
    domscanner.setUrl("http://127.0.0.1:8009/webtest/?default=%3Cscript%3Econsole.log(1234);%3C/script%3E")
    domscanner.setPayloads(payloads)
    domscanner.dealUrl(url)
#     domscanner.scanUrl(payloads)