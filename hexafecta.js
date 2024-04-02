var data;

$(document).ready(function(){
	$('th').css('top', -1);
	$('details').on('toggle', update_details);
	
	var request = new XMLHttpRequest();
	request.open('GET', 'https://arimb.pythonanywhere.com/hexafecta', true);
	request.onload = function(){
		data = JSON.parse(this.response);
		$('div#hexafecta tbody').html('')
		data['hexafecta'].forEach(function(team, i){
			var row = $('div#hexafecta tbody')[0].insertRow(-1);
			for(var i=0; i<8; i++){
				row.insertCell(i).innerHTML = team[i];
			}
		});
		$('div#quinfecta tbody').html('')
		data['quinfecta'].forEach(function(team, i){
			var row = $('div#quinfecta tbody')[0].insertRow(-1);
			for(var i=0; i<8; i++){
				row.insertCell(i).innerHTML = team[i];
			}
		});
		$('div#allteams tbody').html('')
		data['all_teams'].forEach(function(team, i){
			var row = $('div#allteams tbody')[0].insertRow(-1);
			for(var i=0; i<8; i++){
				row.insertCell(i).innerHTML = team[i];
			}
		});
		$('div#loading').css('display', 'none');
		$('span#last-updated').html('Last updated ' + (new Date(this.getResponseHeader("Last-Modified"))).toLocaleString());
		update_details();
	}
	request.onerror = function(err){
		$('div#loading').css('color','red').html('Server Connection Error');
		console.log(err);
	}
	request.send();
});

function update_details(){
	$('div#hexafecta summary').html(($('div#hexafecta details')[0].open?'Hide':'Show')+' '+data['hexafecta'].length+' teams');
	$('div#quinfecta summary').html(($('div#quinfecta details')[0].open?'Hide':'Show')+' '+data['quinfecta'].length+' teams');
	$('div#allteams summary').html(($('div#allteams details')[0].open?'Hide':'Show')+' '+data['all_teams'].length+' teams');
}