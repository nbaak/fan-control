
$('#controls').ready(function(){
	$('.control').click(function(){        
		var status = document.getElementById('control-status-running');        
        var command = $(this)[0].dataset.command;
		var _url = "/api/post/service";

		$.ajax({	
			type: 'POST',
            data: {
             command: command
            },
			url: _url,
			success: function(msg){
                // set status
				window.console.log("send: "+command+" to" +_url);
                window.console.log("recv: "+msg);
                $('#control-status-running')[0].innerHTML = msg;
			}
		});
	});
});
