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
	$("select#year").change(function(){
		reload();
	});
	reload();
});

function load_table(){
	$("tbody#data").empty();
	data.forEach(function(val){
	 	$("tbody#data").append(`
	 		<tr>
	 			<td>`+val[0]+`</td>
	 			<td`+(val[2]==0?" style='color:red;'":"")+`>`+Number(val[1]/(val[1]+val[2])).toFixed(2)+`</td>
	 			<td>`+val[1]+`</td>
	 			<td>`+val[2]+`</td>
	 			<td>`+val[3]+`</td>
	 			<td>`+(val[1]+val[2]+val[3])+`</td>
	 		</tr>`)
	})
	$("span#loading").css("visibility","hidden");
}

function reload(){
	$("span#loading").css("visibility","visible");
	var xhr = createCORSRequest('GET', "https://arimb.ddns.net/winning_season/"+$("select#year").val()+".json");
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
