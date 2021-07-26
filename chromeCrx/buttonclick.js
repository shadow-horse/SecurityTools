var assmname = "";
var assmdomain = "";
var assmswitch = false;

//函数操作定义

$(document).ready(function(){
            $("#onoffswitch").click(function(){
                clickSwitch();
            });

            $("#savebutton").click(function(){
                saveassminfo();
            });

            $("#getbutton").click(function(){
                getassminfo();
            });
        });

function setassmSwitch(status){
    chrome.storage.local.set({assmswitch: status}, function() {
               console.log("store switch is " + status);
            });
}
function getassmSwitch(){
    console.log("get assm switch ");
    chrome.storage.local.get('assmswitch',function(result){
        console.log(result['assmswitch']);
        return result['assmswitch'];
    }
    );
}
//数据初始化
function initassmSwitch(ob){
    console.log("init assm switch status.");
    chrome.storage.local.get('assmswitch',function(result){
        value = result['assmswitch'];
        document.getElementById("onoffswitch").checked = value;

    }
    );
}

function clickSwitch(){
    console.log('click switch');
    checked = document.getElementById("onoffswitch").checked;
    setassmSwitch(checked);
}

function setassminfo(name,domain){
    chrome.storage.local.set({assmname:name},function(){
        console.log("store assm name: " + name);
    });
    chrome.storage.local.set({assmdomain:domain},function(){
            console.log("store assm domain: " + domain);
    });

}

function initassminfo(){
    chrome.storage.local.get('assmname',function(result){
        $("#assmname").val(result['assmname']);
    });
    chrome.storage.local.get('assmdomain',function(result){
            $("#assmdomain").val(result['assmdomain']);
    });
}

function saveassminfo(){
    console.log("保存扫描任务信息...");
    name = $("#assmname").val();
    domain = $("#assmdomain").val();
    if(name && domain){
        name = name.replace(/(^\s*)|(\s*$)/g, '');
        domain = domain.replace(/(^\s*)|(\s*$)/g, '');
        if(name != '' && domain != '') {
            setassminfo(name,domain);
            alert("保存成功！");
            return;
        }
    }
    alert("保存失败，请输入有效内容！");
}

function getassminfo(){
    chrome.storage.local.get('assmswitch',function(status){
                console.log(status['assmswitch']);
            });

}

//初始化
initassmSwitch();
initassminfo();