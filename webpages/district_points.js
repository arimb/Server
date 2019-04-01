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
		reload();
	});

function reload(){
	console.log("run")

	var xhr = createCORSRequest('GET', "https://arimb.ddns.net/"+$("select#year").val()+".json");
	if (!xhr) {
	  throw new Error('CORS not supported');
	}

	xhr.onload = function() {
	 var responseText = xhr.responseText;
	 console.log(responseText);
	 // process the response.
	};

	xhr.onerror = function() {
	  console.log('There was an error!');
	};

	// $.ajax({
	// 	url: "https://arimb.ddns.net/"+$("select#year").val()+".json",
	// 	type: "GET",
	// 	success: function(result){
	// 		console.log(result)
	// 		console.log("success")
	// 	},
	// 	error: function(result){
	// 		console.log(result)
	// 		console.log("fail")
	// 	}
	// });
	console.log("done")
}
