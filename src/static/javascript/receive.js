/** logBox()
 * 	this function loads the log file via AJAX
 * 	into the log div-element!
 */
console = window.console;

function updateElement(ele) {
    console.log(ele);
    var src = ele.dataset.src;  // wonky stuff
    $(ele).load(src);
}

$('#values').ready(function(){
	//var interval = ele.data("interval");
	
	setInterval(function(){
        var elements = document.getElementsByClassName("value");
        
        for (i = 0; i<elements.length; i++){  // I really don't like JS for-each the element is just the index of the element..
            //console.log("element:" + elements[i]);
            updateElement(elements[i]);
        }
             
	}, 5000);
	
});
