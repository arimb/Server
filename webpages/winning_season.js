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
	$("table").floatThead();
	reload();
});

function load_table(){
	$("tbody#data").empty();
	data.forEach(function(val){
	 	$("tbody#data").append(`
	 		<tr>
	 			<td>`+val[0]+`</td>
	 			<td`+(val[2]==0?" style='color:red;'":"")+`>`+Number(100*val[1]/(val[1]+val[2])).toFixed(1)+`</td>
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
	$("span#server_error").css("display","none");
	var xhr = createCORSRequest('GET', "https://arimb.ddns.net/winning_season/"+$("select#year").val()+".json");
	if (!xhr) {
	  throw new Error('CORS not supported');
	}

	xhr.onload = function() {
		// console.log(xhr.responseText);
		try{
			data = JSON.parse(xhr.responseText);
			load_table();
		}catch(err){
			console.log(err);
			$("span#server_error").css("display","block");
			xhr2 = createCORSRequest('GET', "https://arimb.github.io/Server/winning_season/"+$("select#year").val()+".json");
			xhr2.onload = function(){
				data = JSON.parse(xhr2.responseText);
				load_table();
			}
			xhr2.onerror = function(){
				console.log("second error :(");
				console.log(xhr2);
			}
			xhr2.send();
		}
	};

	xhr.onerror = function() {
	  console.log('There was an error!');
	  $("span#server_error").css("display","block");
	  xhr2 = createCORSRequest('GET', "https://arimb.github.io/Server/winning_season/"+$("select#year").val()+".json");
	  xhr2.onload = function(){
	  	data = JSON.parse(xhr2.responseText);
	  	load_table();
	  }
	  xhr2.onerror = function(){
	  	console.log("second error :(");
	  	console.log(xhr2);
	  }
	  xhr2.send();
	};
	
	xhr.send();
	console.log("done")
}
