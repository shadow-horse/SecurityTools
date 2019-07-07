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

1. 页面异步加载时发起的请求  【支持】
2. 页面href="" 的请求      【支持】

		<link rel="stylesheet" type="text/css" href="theme.css" />
		<a href="" />
		
	
3. 页面src属性值，页面动态加载时会自动加载 【支持】
	
		<audio src="someaudio.wav"> 
		<script src=”“ />
		<source src="horse.ogg" type="audio/ogg">  
		<embed src="helloworld.swf" /> 
		<frame src="frame_a.htm" /> 
		<iframe src="" />
		<img src="" />
		<input src="" />
		<video src="movie.ogg" controls="controls"> 
		
4. post表单请求 

		1. 原始的form表单，input参数，点击按钮提交      【支持】
		2. 存在button按钮，事件点击，触发请求 ，不存在前端输入校验  【支持】
		3. 存在button按钮，事件点击，触发请求，存在前端验证参数合法性 【未支持，需要先自动给标签赋值触发，也可考虑JS直接eval】

5. Button事件点击触发的请求 

		1. <input type="button" />，尝试点击 【支持】
		2. <input type="submit" /> ，尝试点击【支持】
		3. <button /> ，尝试点击 【支持】
		4. 以上事件存在前端输入校验  【不支持】

6. 所有带有onxxx属性的事件触发请求    【不支持】

		实现方式类似Button事件的处理，待梳理补充

5. JSON格式请求 
6. 事件点击触发的Ajax请求 
7. location.href / .open() 

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
	
	
### 5. DOMXSS检测方式

1. 检测DOM结构变化  
	
	发送poc后，等待页面加载完成后，静态解析页面，查询是否存在增加的DOM节点，如果存在则认为发生了XSS注入  
	
2. 	检测js代码执行，采用console.log()，检查执行情况

	发送POC后，等待页面加载完毕后（可能需要点击触发某些事件），检查console.log的输出，如果存在对应的输入则认为发生了XSS注入

3. 直接检测文本内容

	发送POC后，可直接检查响应，检查响应是否存在poc代码，如果存在，则可以认为存在疑似风险。文本的直接检测，只是作为补充，对于JSON格式响应或前端框架而言，数据是基于前端处理的，所以不太适用  

4. 针对POC的设计

	针对扫描XSS的POC比较多，因为不同场景，可能触发的POC就不同，还涉及WAF的拦截、编码的绕过等等，此处验证环境，采用最基础的POC；   

	针对POC的设计，可以在扫描时自动增加URL的hash字段+扫描参数，作为POC的一部分，以便检测出POC时，可以对应是哪个请求和参数发起的

### 6. 其它 

1. 预计完成时间  
2. 支持并发爬取 
3. 支持针对一个host的请求限频设置 
4. 获取所有网站CGI信息 







