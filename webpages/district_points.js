$(document).ready(function(){
	reload();
});

function reload(){
	$.ajax({
		url: "https://arimb.ddns.net/getDistrictPoints/"+$("select#year").val(),
		type: "GET",
		success: function(result){
			console.log(result)
		},
		error: function(result){
			console.log(result)
		}
	});
}