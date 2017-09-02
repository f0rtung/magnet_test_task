function ajaxQuery(action, data, method, sucCallback, async = true){
	$.ajax({
		url: action,
		data: data,
		type: method,
		async: async,
		success: function(response){
			   sucCallback(response);
		}
	});
}