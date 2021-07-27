;(function(){

	var _onload = window.onload;

	window.onload = function()
	{
		if(_onload) { _onload(); }

        var api = window.default;

        if(window.api) { api = window.api; }

		$.ajax({
        method:"GET",
        url: window.api,
        dataType:"jsonp",
        jsonpCallback:"callback",
        success:function(data){
            if(window.wrapper) { $("#"+window.wrapper).html(baidu.template(window.content,data)); }
            else { document.write(baidu.template(window.content,data)); }
        }
    });
	}

})();