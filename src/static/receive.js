/** logBox()
 * 	this function loads the log file via AJAX
 * 	into the log div-element!
 */
console = window.console;

$('#logBox').ready(function(){
	var ele = $('#logBox');
	var src = ele.data("src");
	var interval = ele.data("interval");
	
	console.log(src);
	setInterval(function(){
		$('#logBox').load(src);
		$('#logBox').scrollTop(250);
	}, interval);
	
});
