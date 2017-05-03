var url = window.location.href;
//console.log(baseurl)

function header(){
	var header_path = "../_tpl/header.html"
	$("#header").load(header_path); 
	//console.log(url + header_path)
}

function footer(){
	var footer_path = "../_tpl/footer.html"
	$("#footer").load(footer_path); 
	//console.log(url + footer_path)
}

function dv_1b(){

	// Main variables
	var container = $("#dv_1b");
	var w = Math.floor(container.width()),
		h = Math.floor(container.height());

	var margin = {top: 10, left:10, bottom:10, right:10};
	var width = w - margin.left - margin.right,
		height = h - margin.top - margin.bottom;
	
	// General layout
	var svg = d3.select("#dv_1_2").append("svg")
		.attr("height", height + margin.top + margin.bottom)
		.attr("width", width + margin.left + margin.right)
		.append("g")
		.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
		
	//console.log(w);
}

$( document ).ready(function() {
	header();
	footer();

	dv_1b();
});