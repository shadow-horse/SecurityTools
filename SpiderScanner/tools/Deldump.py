#!/usr/bin/python

'''
对传入的URL列表去重
'''
import hashlib
import json
from urllib.parse import urlparse
from urllib.parse import parse_qs

class Deldump:
            
    '''
    针对传入的URL列表，通过计算md5的方式进行去重
    MD5(域名+PATH+参数)
    目前无法处理POST请求参数中JSON格式的去重
    '''
    def deldumpurls(self,urllists):
        url = {}
        for oneurl in urllists:
            url_parse = urlparse(oneurl['url'])
            url_params = parse_qs(url_parse.query)
            url_postdata = parse_qs(oneurl['postdata'])
            #协议+域名+路径
            md5_r = url_parse.scheme +"://"+ url_parse.netloc + url_parse.path;
            for param in sorted(url_params.keys()):
                md5_r = md5_r + "?" + param + "=&"
            for param in sorted(url_postdata.keys()):
                md5_r = md5_r + "?" + param + "=&"
            md5_str = hashlib.md5(md5_r.encode('utf8')).hexdigest()
            if not (md5_str in url.keys()):
                url[md5_str] = oneurl
        
        return url
            
            