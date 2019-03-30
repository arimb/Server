$(document).ready(function(){
	reload();
});

function reload(){
	$.ajax({
		url: "http://192.168.1.16:5000/getDistrictPoints/"+$("select#year").val(),
		type: "GET",
		success: function(result){
			console.log(result)
		},
		error: function(result){
			console.log(result)
		}
	});
}