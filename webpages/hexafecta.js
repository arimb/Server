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
	 	$("tbody#data").append(`
	 		<tr>
	 			<td>`+key+`</td>
	 			<td>`+data["hexafecta"][key]["IndDsn"]+`</td>
	 			<td>`+data["hexafecta"][key]["Qual"]+`</td>
	 			<td>`+data["hexafecta"][key]["Creativ"]+`</td>
	 			<td>`+data["hexafecta"][key]["EngEx"]+`</td>
	 			<td>`+data["hexafecta"][key]["Cntrl"]+`</td>
	 			<td>`+data["hexafecta"][key]["Auton"]+`</td>
	 		</tr>`)
	})
	sorttable.innerSortFunction.apply($("th:contains('Team')")[0], []);
	sorttable.innerSortFunction.apply($("th:contains('Adj DP')")[0], []);
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
