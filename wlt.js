$(document).ready(function(){
	$('select#year').change(update);
	$('th').css('top', -1);
	update();
});
function update(){
	$('span#loading').css('display', 'block');
	$('tbody').html('');
	$('span#last-updated').html('');

	var request = new XMLHttpRequest();
	var url = 'https://arimb.pythonanywhere.com/wlt/' + $('select#year').children('option:selected')[0].value;
	request.open('GET', url, true);
	request.onload = function(){
		var data = JSON.parse(this.response);
		data.forEach(function(team, i){
			var pct = (team[1][1]+team[1][3]/2)/team[1].slice(1,4).reduce((a,b)=>a+b,0);
			var row = $('tbody')[0].insertRow(-1);
			row.insertCell(0).innerHTML = (i==0?1:pct==((data[i-1][1][1]+data[i-1][1][2]/2)/data[i-1][1].slice(1,4).reduce((a,b)=>a+b,0))?'':i+1);
			row.insertCell(1).innerHTML = team[1][0];
			row.insertCell(2).innerHTML = pct.toFixed(2);
			row.insertCell(3).innerHTML = team[1][1];
			row.insertCell(4).innerHTML = team[1][2];
			row.insertCell(5).innerHTML = team[1][3];
			row.insertCell(6).innerHTML = team[1].slice(1,4).reduce((a,b)=>a+b,0);
			if(pct == 1)
				$('tr:last > td:nth-child(3)').css('color', 'red')
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