function on_scroll(){
	var scrollTop = document.body.scrollTop || document.documentElement.scrollTop;
	var width = $( document ).width()
	var menu = $(".vis_invis")
	var header = $("header")
	var home = $("#home")

	if (width > 800){
		if (scrollTop > 120) {
			menu.addClass("visible");
			header.addClass("header_visible");
			//console.log(scrollTop);
		}
		else {
			menu.removeClass("visible");
			header.removeClass("header_visible");
		}
	}
	else {
		if (scrollTop > 20) {
			menu.addClass("visible");
			header.addClass("header_visible");	
		}
		else {
			menu.removeClass("visible");
			header.removeClass("header_visible");
		}
	}
}

function menu() {
	var nav = document.getElementById("mySidenav")
	//console.log(nav)

	function openNav() {
		$("#open_nav").on("click", function(){
			nav.style.left = "0px";
			//console.log("open nav")
		});
	}

	function closeNav() {
		$("#close_nav").on("click", function(){
			nav.style.left = "-250px";
			//console.log("close nav")

			$("a").on("click", function(){
				nav.style.left = "0px";
			})
		})
	}

	openNav();
	closeNav();
}

function page_size(loading_time){
	
	console.group("website performance");

	var dom_elements = $('*').length;
	console.log("DOM elements: " + dom_elements); 

	var bytes = $('html').html().length,
		kbytes = bytes / 1024;
	console.log("kbytes: " + kbytes.toFixed(1) + " (max 2000)" );
	console.log("loading: " + loading_time + "ms (max 2000ms)");

	console.groupEnd();

}

$( document ).ready(function() {
	setTimeout(menu,300) // I give the javascript the time to load the nav
	window.addEventListener("scroll", on_scroll);
});