$(document).ready(function(){
	$('select#year').change(update);
	update();
});

function update(){
	$('span#loading').css('display', 'block');
	$('span#last-updated').html('');

    var year = $('select#year').children('option:selected')[0].value;

    $('div#images').html(
        '<img src="https://arimb.pythonanywhere.com/alliance_distribution/' + year + '_Winners.png" alt="' + year + ` Winners" /> <br>
        <img src="https://arimb.pythonanywhere.com/alliance_distribution/` + year + '_Finals.png" alt="' + year + ` Finals" /> <br>
        <img src="https://arimb.pythonanywhere.com/alliance_distribution/` + year + '_Semifinals.png" alt="' + year + ' Semifinals" />');
	
	$('span#loading').css('display', 'none');
}