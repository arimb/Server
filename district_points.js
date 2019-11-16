var header, sticky;
$(document).ready(function(){
	header = $('thead')[0];
	sticky = header.offsetTop;
	window.onscroll = function(){
		if (window.pageYOffset > sticky){
			header.classList.add("sticky");
		}else{
			header.classList.remove("sticky");
		}
	}
	$('select#year').change(update);
	$('input#awards').change(update);
	update();
});

function update(){
	$('span#loading').css('display', 'block');
	$('tbody').html('');
	$('span#last-updated').html('');

	var request = new XMLHttpRequest();
	var url = 'https://arimb.pythonanywhere.com/district_points/' + $('select#year').children('option:selected')[0].value + ($('input#awards')[0].checked ? '_awards' : '');
	request.open('GET', url, true);
	request.onload = function(){
		var data = JSON.parse(this.response);
		data.forEach(function(team, i){
			var row = $('tbody')[0].insertRow(-1);
			row.insertCell(0).innerHTML = (i==0?1:data[i-1][1][1][0]==team[1][1][0]?'':i+1);
			row.insertCell(1).innerHTML = team[0];
			row.insertCell(2).innerHTML = team[1][1][0].toFixed(2);
			row.insertCell(3).innerHTML = team[1][1][1].toFixed(2);
			row.insertCell(4).innerHTML = team[1][1][2].toFixed(2);
			row.insertCell(5).innerHTML = team[1][1][3].toFixed(2);
			row.insertCell(6).innerHTML = team[1][1][4];
		});
		$('span#loading').css('display', 'none');
		$('span#last-updated').html('Last updated ' + this.getResponseHeader("Last-Modified"));
	}
	request.onerror = function(err){
		$('span#loading').css('color','red').html('Server Connection Error');
		console.log(err);
	}
	request.send();
}