$('#roll').ready(function(){
	$('#roll').click(function(){
		var dicesF = document.getElementById('numberOfDices');
		var sitesF = document.getElementById('numberOfSites');
		var charF  = document.getElementById('charSend');
		var roomF  = document.getElementById('roomSend');

		// Url to work with the dice
		var _url = "action/logWriter.php";

		$.ajax({		
			type: 'POST',
			url: _url,
			data: {
				numberOfDices: dicesF.value,
				numberOfSites: sitesF.value,
				charName: charF.value,
				room: roomF.value
			},
			success: function(msg){
				/*window.console.log("sende: Würfel "+dicesF.value + ", Augen "+sitesF.value+", Raum "+ roomF.value+", Char "+charF.value);
				window.console.log("nach: "+_url)
				window.console.log($(this));*/				
			}
		});
	});
});