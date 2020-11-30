



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
    
    $('#new-start-value').ready(function(){        
        var url = $('#new-start-value').data("src");        
        $.get(url, function(data) {
            $('#new-start-value')[0].value = parseFloat(data);
        });
    });
    
    $('#new-stop-value').ready(function(){        
        var url = $('#new-stop-value').data("src");        
        $.get(url, function(data) {
            $('#new-stop-value')[0].value = parseFloat(data);
        });
    });
        
	$('#new-start-stop').click(function(){        
        var new_start = parseFloat(document.getElementById('new-start-value').value);
        var new_stop  = parseFloat(document.getElementById('new-stop-value').value);
        
        var _url = "/api/post/start-stop-temperatures";
        
        message_box = $('#new-values-status')[0];
        message_box.innerText = "";
        
        if (validate_values(new_stop, new_start)){
            // start
                       
            if (new_start){
                $.ajax({
                    type: 'POST',
                    data: {
                        command: 'start',
                        value: new_start
                    },
                    url: _url,
                    success: function(msg){
                        // set status
                        message_box.innerText += msg + "\n";
                    }
                });
            }
            
            // stop
            if (new_stop){
                $.ajax({	
                    type: 'POST',
                    data: {
                        command: 'stop',
                        value: new_stop
                    },
                    url: _url,
                    success: function(msg){
                        // set status
                        message_box.innerText += msg + " ";
                    }
                });
            }
        }
        else {
            message_box.innerText = "Stop value needs to be smaller then the start value!";
        }
        
	});
});
