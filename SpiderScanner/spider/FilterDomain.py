#!/usr/bin/python
'''
检查域名是否需要过滤
'''
from urllib.parse import urlparse

class FilterDomain():
    def __init__(self):
        self.domain = '' 
        
    def isfilter(self,url,specdomain):
        res = urlparse(url)
        print(res)
        if specdomain == '':
            self.domain = res.netloc
        else:
            self.domain = specdomain
        
        if res.netloc.endswith(self.domain):
            return True
        else:
            return False
        
