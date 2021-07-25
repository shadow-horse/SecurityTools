var assmname = localStorage.assmname;
var assmdomain = localStorage.assmdomain;
var assmbutton = localStorage.assmbutton;
var assmscan = localStorage.assmscan;

console.log(assmname);
assmbutton = assmbutton?assmbutton:'false';


if(assmbutton === 'true')
{
    console.log('====');
    value = document.getElementsById("onoffswitch");
    console.log(value);

    $("#onoffswitch").attr("checked",true);
}else
{
    $("#onoffswitch").attr("checked",false);
}

if(assmname !=""){
    $("#assmname").val(localStorage.assmname);
    $("#assmdomain").val(localStorage.assmdomain);
}

function setassmSwitch(onoff){
    chrome.storage.local.set({'assmswitch': onoff}, function() {
            console.log("store switch is " + onoff);
            });
}

function onClickHander(obj){
            console.log("click off/on  ....");
            onoff = document.getElementsByName("onoffswitch")[0].checked;
            console.log(onoff);
			console.log("在ON的状态下");
			setassmSwitch
}

function saveassminfo(){
    console.log("保存扫描任务信息...");
    name = $("#assmname").val();
    domain = $("#assmdomain").val();
    if(name && domain){
        name = name.replace(/(^\s*)|(\s*$)/g, '');
        domain = domain.replace(/(^\s*)|(\s*$)/g, '');

        if(name != '' && domain != '') {
            localStorage.assmname = name;
            localStorage.assmdomain = domain;
            alert("保存成功！");
            return;
        }
    }
    alert("保存失败，请输入有效内容！");

}

