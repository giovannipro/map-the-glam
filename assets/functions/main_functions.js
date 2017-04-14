function menu() {
	var nav = document.getElementById("mySidenav")

	function openNav() {
		$("#open_nav").on("click", function(){
			nav.style.left = "0px";

		});
	}

	function closeNav() {
		$("#close_nav").on("click", function(){
			nav.style.left = "-250px";
		})
	}

	openNav();
	closeNav();
}

$( document ).ready(function() {
	setTimeout(menu,100) // I give the javascript the time to load the nav
});