#!/usr/bin/python
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
        

if __name__ == '__main__': 
    fd = FilterDomain()
    flag = fd.isfilter('http://47.104.218.243/AWDV/login.php:password', '218.243')
    print(flag)