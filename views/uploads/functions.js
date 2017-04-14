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

$( document ).ready(function() {
	header();
	footer();
});