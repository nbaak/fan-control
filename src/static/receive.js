/** logBox()
 * 	this function loads the log file via AJAX
 * 	into the log div-element!
 */
console = window.console;

function updateElement(elementId) {
    var element = $(elementId);
    var src = element.data("src");
    
    console.log(src);
    $(elementId).load(src);
}

$(document).ready(function(){
	//var interval = ele.data("interval");
	
	console.log(src);
	setInterval(function(){
        updateElement('#servicestatus');
	}, 5000);
	
});
