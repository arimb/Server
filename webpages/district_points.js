$(document).ready(function(){
	reload();
});

function reload(){
	console.log("run")
	$.ajax({
		url: "http://arimb.ddns.net:5000/getDistrictPoints/"+$("select#year").val(),
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
