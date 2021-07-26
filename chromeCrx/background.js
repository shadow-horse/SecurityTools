//上报请求
function sendReqserver(reqid,contens){
    var xhr = new XMLHttpRequest();
    console.log(reqid);
    //防止循环监听，过略上报的域名
    xhr.open('GET', 'http://47.104.218.243/ssrf/ssrf.php?rand='+reqid, true);

    xhr.onload = function () {
       // 请求结束后,在此处写处理代码
       console.log('send success~~')
    };

    xhr.send(null);

}
// 监听函数, 当符合代理配置的, 重写请求路径
function getRequests (details) {
//  console.log(details);
  console.log("===========================================================");
  console.log("reqid:  " + details['requestId']);
  console.log("url:    " + details['url']);
  console.log("method: " + details['method']);
  if(details['method'] == 'POST'){
    console.log(details['requestBody']);
    let requestBody = details['requestBody'];
    if(details['type'] == 'main_frame'){
        console.log("reqbody:  ");
        console.log(requestBody['formData']);
    }else if(details['type'] == 'xmlhttprequest'){
        console.log("reqbody:  ");
        console.log(requestBody['raw']);
    }
  }else
  {
    console.log('method get！')
  }
  return {cancel: false}
}
function getheaders(details){
//    console.log(details);
    console.log("********************************");
    console.log("reqid: " + details['requestId']);
    console.log("requestHeaders: ")
    console.log(details['requestHeaders'])

//    sendReqserver(details['requestId'],"");
}
function del_callback (parameters) { /* ... */ }

// 添加代理监听方法
function addRequestlistener () {
  console.log('addRequestlistener=====================');
  urls = assmdomain.split(',');
  all_urls = "";
  for (i = 0; i<urls.length;i++){
     urls[i] = "*://" + urls[i] +"/*";
     console.log(urls[i]);
  }

  chrome.webRequest.onBeforeRequest.addListener(
    getRequests,
    {urls: urls},
    ["extraHeaders","requestBody"]
  )
  // alert(chrome.webRequest.onBeforeRequest.hasListeners())
}
// 移除代理监听
function delRequestlistener () {
    console.log('delRequestlistener=====================');
      urls = assmdomain.split(',');
      all_urls = "";
      for (i = 0; i<urls.length;i++){
         urls[i] = "*://" + urls[i] +"/*";
         console.log(urls[i]);
      }

  chrome.webRequest.onBeforeRequest.removeListener(
    getRequests,
    {urls: urls},
    ["extraHeaders","requestBody"]
  )
  // alert(chrome.webRequest.onBeforeRequest.hasListeners())
}

//添加headers监听
function addHeaderlistener(){
    console.log('addHeaderlistener=====================');
    urls = assmdomain.split(',');
    all_urls = "";
    for (i = 0; i<urls.length;i++){
         urls[i] = "*://" + urls[i] +"/*";
         console.log(urls[i]);
    }
    chrome.webRequest.onBeforeSendHeaders.addListener(
        getheaders,
        {urls:urls},['extraHeaders','requestHeaders']);
}
function delHeaderlistener(){
    console.log('delHeaderlistener=====================');
        urls = assmdomain.split(',');
        all_urls = "";
        for (i = 0; i<urls.length;i++){
             urls[i] = "*://" + urls[i] +"/*";
             console.log(urls[i]);
        }

    chrome.webRequest.onBeforeSendHeaders.removeListener(
        getheaders,
        {urls: urls},['extraHeaders','requestHeaders']);
}


// 注册回调，当收到请求的时候触发
chrome.extension.onRequest.addListener(({ tabId, args }) => {
  console.log('requrst listener');

  // 在给定tabId的tab页中执行脚本
  chrome.tabs.executeScript(tabId, {
    code: `console.log(...${JSON.stringify(args)});`,
  });

  //发起请求
});


var assmname = "";
var assmdomain = "";
var assmswitch = false;

function getassminfo(){
    chrome.storage.local.get('assmname',function(result){
            assmname = result['assmname'];
        });
        chrome.storage.local.get('assmdomain',function(result){
               assmdomain = result['assmdomain'];
        });
        chrome.storage.local.get('assmswitch',function(result){
               assmswitch = result['assmswitch'];
         });
}




//初始化,设置监听的启停
function initassmswitch(){
    chrome.storage.local.get('assmswitch',function switchstatus(result){
                                              value = result['assmswitch'];
                                              if(value){
                                                  console.log('add listener.......');
                                                  addRequestlistener();
                                                  addHeaderlistener();
                                              }else{
                                                      console.log('close listener.......');
                                                      delRequestlistener();
                                                      delHeaderlistener();
                                                   }
                                          });
}
getassminfo();
setTimeout(initassmswitch,1000);

function testassminfo(){
    console.log('assmname: ' + assmname);
    console.log('assmdomain: ' + assmdomain);
}

setTimeout(testassminfo,100);



function updateListener()
{
    //清理
    delHeaderlistener();
    delRequestlistener();

    console.log('assm switch is ' + assmswitch);
    if(assmswitch){
        console.log('add listener.......');
        addHeaderlistener();
        addRequestlistener();
    }else{
        console.log('close listener.......');

    }
}

//增加存储监听按钮，修改配置信息
chrome.storage.onChanged.addListener((changes, namespace) => {
    //如果配置信息修改，则重新设置监听器
    getassminfo();
    setTimeout(updateListener,1000);

})