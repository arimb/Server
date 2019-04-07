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

  } else {

    // Otherwise, CORS is not supported by the browser.
    xhr = null;

  }
  return xhr;
}

$(document).ready(function(){
	$("select#year").change(function(){
		console.log("hit")
		reload();
	});
	$("input#awards").change(function(){
		load_table();
	});
	reload();
});

function load_table(){
	$("tbody#data").empty();
	Object.keys(data).forEach(function(key){
	 	$("tbody#data").append(`
	 		<tr>
	 			<td>`
	 			// +($("input#awards").is(":checked") ? data[key]["award_rank"] : data[key]["rank"])+`</td>
	 			// <td>`
	 			+key+`</td>
	 			<td>`+Number(data[key]["adj"]).toFixed(2)+`</td>
	 			<td>`+Number(data[key]["adj_qual"]).toFixed(2)+`</td>
	 			<td>`+Number(data[key]["adj_alliance"]).toFixed(2)+`</td>
	 			<td>`+Number(data[key]["adj_playoff"]).toFixed(2)+`</td>
	 			<td>`+data[key]["num_events"]+`</td>
	 		</tr>`)
	})
	sorttable.innerSortFunction.apply($("th:contains('Adj DP')")[0], []);
}

function reload(){
	var xhr = createCORSRequest('GET', "https://arimb.ddns.net/district_points/"+$("select#year").val()+".json");
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
