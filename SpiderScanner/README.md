## 基于Python的爬虫扫描器

### 1. 选定爬虫的环境 

https://weibo.com/  

### 2. 环境配置

1. python3.0  Mac  
2. pip isntall selenium 模拟浏览器  
3. pip install beautifulsoup4
4. pip install lxml
5. 安装phantomjs,设置环境变量，代码中设置路径 
6. pip install requests

### 3. 爬虫获取的链接

1. 页面异步加载时发起的请求  
2. 页面href="" 的请求 
3. 页面src属性值 
4. post表单请求 
5. JSON格式请求 
6. 事件点击触发的Ajax请求 


### 4. DOM XSS环境搭建
1. document.write直接输出导致的XSS
	
		document.write("<P>"+domxss1 + "</p>");
		document.write("<a href=\"" +domxss1 + "\">超链接</a>");

2. 使用innerHTML输出导致XSS

		document.getElementById("domxss2").innerHTML="<p>"+domxss2+"</p>";

3. 使用location/location.href/location.replace/iframe.src造成的XSS  

		location.href=domxss3;  
	
4. setTimeout/setInterval造成的XSS

		setTimeout("showText('"+domxss4+"')",2000);
		
整理的API： 

	document.location
	document.URL
	document.URLUnencoded
	document.referrer
	window.location
	
	document.write()
	document.writeln()
	document.boby.innerHtml
	eval()
	window.execScript()
	window.setInterval()
	window.setTimeout()
	
	document.location
	document.URL
	document.open()
	window.location.href
	window.navigate()
	window.open
	
	






