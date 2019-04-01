$(document).ready(function(){
	reload();
});

function reload(){
	console.log("run")
	$.ajax({
		url: "https://arimb.ddns.net/"+$("select#year").val()+".json",
		type: "GET",
		success: function(result){
			console.log(result)
			console.log("success")
		},
		error: function(result){
			console.log(result)
			console.log("fail")
		}
	});
	console.log("done")
}
