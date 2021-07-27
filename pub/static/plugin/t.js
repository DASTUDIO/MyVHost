;(function(){

	var _onload = window.onload;

	window.onload = function()
	{
		if(_onload) { _onload(); }

        window.dorender = function(api,content,target){

		$.ajax({
        method:"GET",
        url: api,
        dataType:"jsonp",
        jsonpCallback:"callback",
        success:function(data){
            if(data) { $("#"+target).html(baidu.template(content,data)); }
            else { document.write(baidu.template(content,data)); }
        }
    });
    }

	}

})();