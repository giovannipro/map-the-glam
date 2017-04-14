var baseurl = window.location.href;
//var baseurl = document.location.origin;
//console.log(baseurl)

function header(){
	var header_path = "views/_tpl/header.html"
	var h_path = baseurl + header_path
	$("#header").load(h_path); 
	//console.log(baseurl + header_path)
}

function footer(){
	var footer_path = "views/_tpl/footer.html"
	var f_path = baseurl + footer_path
	$("#footer").load(f_path); 
	//console.log(f_path)
}

$( document ).ready(function() {
	header();
	footer();
});