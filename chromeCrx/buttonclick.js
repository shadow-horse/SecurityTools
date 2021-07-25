var assmname = localStorage.assmname;
var assmdomain = localStorage.assmdomain;
var assmbutton = localStorage.assmbutton;
var assmscan = localStorage.assmscan;

assmbutton = assmbutton?assmbutton:'false';
console.log(assmbutton);
if(assmbutton === 'true')
{
    console.log('====')
    $("#onoffswitch").attr("checked",true);
}else
{
    $("#onoffswitch").attr("checked",false);
}


function onClickHander(obj){

            console.log($("#onoffswitch").is(':checked'));

            if ($("#onoffswitch").is(':checked')) {
			    console.log("在ON的状态下");
			    localStorage.assmbutton = true;
		    } else {
			    console.log("在OFF的状态下");
			    localStorage.assmbutton = false;
		    }

        }


