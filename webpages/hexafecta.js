var data;

function createCORSRequest(method, url) {
  var xhr = new XMLHttpRequest();
  if ("withCredentials" in xhr) {

    // Check if the XMLHttpRequest object has a "withCredentials" property.
    // "withCredentials" only exists on XMLHTTPRequest2 objects.
    xhr.open(method, url, true);

  } else if (typeof XDomainRequest != "undefined") {

    // Otherwise, check if XDomainRequest.
    // XDomainRequest only exists in IE, and is IE's way of making CORS requests.
    xhr = new XDomainRequest();
    xhr.open(method, url);
    xhr.setRequestHeader('max-age',3600);

  } else {

    // Otherwise, CORS is not supported by the browser.
    xhr = null;

  }
  return xhr;
}

$(document).ready(function(){
	reload();
});

function load_table(){
	$("tbody#hexafecta").empty();

	Object.keys(data["hexafecta"]).forEach(function(key){
	 	$("tbody#hexafecta").append(`
	 		<tr>
	 			<td>`+key+`</td>
	 			<td>`+data["hexafecta"][key][0]+`</td>
	 			<td>`+data["hexafecta"][key][1]+`</td>
	 			<td>`+data["hexafecta"][key][2]+`</td>
	 			<td>`+data["hexafecta"][key][3]+`</td>
	 			<td>`+data["hexafecta"][key][4]+`</td>
	 			<td>`+data["hexafecta"][key][5]+`</td>
	 		</tr>`)
	})

	$("summary#quinfecta").html("See "+Object.keys(data["quinfecta"]).length+" teams")
	Object.keys(data["quinfecta"]).forEach(function(key){
	 	$("tbody#quinfecta").append(`
	 		<tr>
	 			<td>`+key+`</td>
	 			<td>`+data["quinfecta"][key][0]+`</td>
	 			<td>`+data["quinfecta"][key][1]+`</td>
	 			<td>`+data["quinfecta"][key][2]+`</td>
	 			<td>`+data["quinfecta"][key][3]+`</td>
	 			<td>`+data["quinfecta"][key][4]+`</td>
	 			<td>`+data["quinfecta"][key][5]+`</td>
	 			<td>`+data["quinfecta"][key][6]+`</td>
	 		</tr>`)
	})

	$("summary#all_teams").html("See "+Object.keys(data["all_teams"]).length+" teams")
	Object.keys(data["all_teams"]).forEach(function(key){
	 	$("tbody#all_teams").append(`
	 		<tr>
	 			<td>`+key+`</td>
	 			<td>`+data["all_teams"][key][0]+`</td>
	 			<td>`+data["all_teams"][key][1]+`</td>
	 			<td>`+data["all_teams"][key][2]+`</td>
	 			<td>`+data["all_teams"][key][3]+`</td>
	 			<td>`+data["all_teams"][key][4]+`</td>
	 			<td>`+data["all_teams"][key][5]+`</td>
	 			<td>`+data["all_teams"][key][6]+`</td>
	 		</tr>`)
	})

	$("span#loading").css("visibility","hidden");
}

function reload(){
	$("span#loading").css("visibility","visible");
	var xhr = createCORSRequest('GET', "https://arimb.ddns.net/hexafecta.json");
	if (!xhr) {
	  throw new Error('CORS not supported');
	}

	xhr.onload = function() {
	 // console.log(xhr.responseText);
	 data = JSON.parse(xhr.responseText);
	 load_table();
	};

	xhr.onerror = function() {
	  console.log('There was an error!');
	};
	
	xhr.send();
	console.log("done")
}
