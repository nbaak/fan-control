



function isNumber(number) {
    if (typeof(number) == 'number'){
        return true;
    }else {
        return false;
    }
}

function isString(string){
    if(string && typeof(string) == "string")
        return true;
    else
        return false;
}

function validate_values(min, max) {
    if (isNumber(max) && isNumber(min)){
        if (max > min) {
            return true;
        } else {
            return false;
        }
    }
    else {
        return false;
    }      
}


$('#control-edge-temperatures').ready(function(){
    
    
    // TODO: make this work.. if the page show up initialy, values should be set in input box
    $('#new-start-value').ready(function(){
        $('#old-start-value').ready(function(){
            document.getElementById('new-start-value').value = parseFloat(document.getElementById('old-start-value').innerText);
            window.console.log('start ' + document.getElementById('old-start-value').innerText);
        });      
    });
    
    $('#new-stop-value').ready(function(){
        $('#old-stop-value').ready(function(){
            document.getElementById('new-stop-value').value = parseFloat(document.getElementById('old-stop-value').innerText);
            window.console.log('stop ' + document.getElementById('old-stop-value').innnerText);
        });        
    });
    
	$('#new-start-stop').click(function(){        
		var old_start = parseFloat(document.getElementById('old-start-value').innerText);
        var old_stop  = parseFloat(document.getElementById('old-stop-value').innerText);
        
        var new_start = parseFloat(document.getElementById('new-start-value').value);
        var new_stop  = parseFloat(document.getElementById('new-stop-value').value);
        
        var _url = "/api/post/start-stop-temperatures";
        
        if (validate_values(new_stop, new_start)){
            // start
            if (old_start != new_start){
                $.ajax({	
                    type: 'POST',
                    data: {
                        command: 'start',
                        value: new_start
                    },
                    url: _url,
                    success: function(msg){
                        // set status
                        window.console.log("recv: "+msg);
                        $('#control-status-running').innerHTML = msg;
                    }
                });
            }
            
            // stop
            if (old_stop != new_stop){
                $.ajax({	
                    type: 'POST',
                    data: {
                        command: 'stop',
                        value: new_stop
                    },
                    url: _url,
                    success: function(msg){
                        // set status
                        window.console.log("recv: "+msg);
                        $('#new-values-status').innerHTML = msg;
                    }
                });
            }
        }
	});
});
