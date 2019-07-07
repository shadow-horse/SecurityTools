from urllib.parse import urlparse
from urllib.parse import parse_qs
import json
url = "https://weibo.com?a=b&c=a&b=b&aa=c&ab=c&aa=c&dc=df&fd=fd"

res =  urlparse(url)
print(res)
print(res.scheme)
print(res.netloc)
print(res.query)

pars = parse_qs(res.query)

print(pars)

for a in sorted(pars.keys()):
    print(a)
    
if('d' in pars.keys()):
    print(True)
else:
    print(False)
