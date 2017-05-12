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

$( document ).ready(function() {
	setTimeout(menu,300) // I give the javascript the time to load the nav
});