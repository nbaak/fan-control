/** logBox()
 * 	this function loads the log file via AJAX
 * 	into the log div-element!
 */
console = window.console;


function updateElements(elements) {
    for (i = 0; i<elements.length; i++){  // I really don't like JS for-each the element is just the index of the element..
        updateElement(elements[i]);
    }
}

function updateElement(ele) {
    //console.log(ele);
    var src = ele.dataset.src;  // wonky stuff
    $(ele).load(src);
}

$('#values').ready(function(){
	// initial
    var elements = document.getElementsByClassName("update");        
    updateElements(elements);    
    
	setInterval(function(){
        var elements = document.getElementsByClassName("update");        
        updateElements(elements);
             
	}, 5000);
});


$('#control-edge-temperatures').ready(function(){
    // initial
    var elements = document.getElementsByClassName("update-slow");        
    updateElements(elements);
    
    setInterval(function(){
        var elements = document.getElementsByClassName("update-slow");        
        updateElements(elements);
             
	}, 60000);
});
