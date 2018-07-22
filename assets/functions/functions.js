var baseurl = window.location.href;
var transition = 300;
var start = new Date();

var curve = [
	"d3.curveStep",
	"d3.curveStepBefore",
	"d3.curveStepAfter",
	"d3.curveBasis",
	"d3.curveCardinal",
	"d3.curveMonotoneX",
	"d3.curveCatmullRom"
]

var easing = [
	"easeElastic",
	"easeBounce",
	"easeLinear",
	"easeSin",
	"easeQuad",
	"easeCubic",
	"easePoly",
	"easeCircle",
	"easeExp",
	"easeBack",
	"easeExpOut",
	"easeExpInOut",
	"easeCircleOut"
];

var colors = {
	item_a:"hsl(196, 96%, 40%)",
	item_b:"hsl(196, 96%, 30%)",
	item_c:"hsl(196, 96%, 20%)",
	a:"red",
	b:"blue",
	c:"green",
	d:"#29b29d",
	e:"#0686da",
	f:"#ef9227",
	g:"#84c233",
	myAxis:"#636060"
};

function cookie_intro(){
	
	function setCookie(c_name,value,exdays){var exdate=new Date();exdate.setDate(exdate.getDate() + exdays);var c_value=escape(value) + ((exdays==null) ? "" : "; expires="+exdate.toUTCString());document.cookie=c_name + "=" + c_value;}
	function getCookie(c_name){var c_value = document.cookie;var c_start = c_value.indexOf(" " + c_name + "=");if (c_start == -1){c_start = c_value.indexOf(c_name + "=");}if (c_start == -1){c_value = null;}else{c_start = c_value.indexOf("=", c_start) + 1;var c_end = c_value.indexOf(";", c_start);if (c_end == -1){c_end = c_value.length;}c_value = unescape(c_value.substring(c_start,c_end));}return c_value;}
	function delCookie(name){document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';}

	if (!getCookie('first_time')){ // if false
		setCookie('first_time',true); // if true
		intro();
	}
}

function intro(){
	console.log("intro")
}

function header(){
	var header_path = "views/_tpl/header_main.html"
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

function dataviz_docu(){
	var timeline_uploads_path = "views/_tpl/timeline_uploads_docu.html"
	var timeline_uploads_path_ = baseurl + timeline_uploads_path
	$("#timeline_uploads_docu").load(timeline_uploads_path_);
	//console.log(dataviz_docu)
}

function open_docu(dataviz){

	var my_class = "open_panel";
	var invisible = "invisible"
	
	var docu_container  = $("#" + dataviz + "_docu_container")

	var protocol_button = $("#" + dataviz + "_open_protocol")
	var protocol = $("#" + dataviz + "_protocol")

	var data_button = $("#" + dataviz + "_open_data")
	var data = $("#" + dataviz + "_data")

	function open_protocol(){
		protocol.show()
		data.hide()
	}
	function open_data(){
		data.show()
		protocol.hide()
	}

	protocol_button.click(function(){
		//console.log(dataviz)

		data_button.removeClass("selected")
		protocol_button.addClass("selected")

		if (docu_container.hasClass("open_panel")) {
			if (data.is(":visible")) {
				protocol.show()
				data.hide()
			}
			else {
				protocol_button.removeClass("selected")
				protocol.hide()
				docu_container.removeClass("open_panel")
			}
		}
		else {
			setTimeout(open_protocol,transition)
			docu_container.addClass("open_panel")
		}
	})

	data_button.click(function(){
		protocol_button.removeClass("selected")
		data_button.addClass("selected")

		if (docu_container.hasClass("open_panel")) {
			if (protocol.is(":visible")) {
				data.show()
				protocol.hide()
			}
			else {
				data_button.removeClass("selected")
				data.hide()
				docu_container.removeClass("open_panel")
			}
		}
		else {
			setTimeout(open_data,transition)
			docu_container.addClass("open_panel")
		}	
	})
}

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
	var nav = document.getElementById("mySidenav");

	function openNav() {
		$("#open_nav").on("click", function(){
			nav.style.left = "0px";
		});
	}

	function closeNav() {
		$("#close_nav").on("click", function(){
			nav.style.left = "-250px";
		})
		$(".section_end").on("click", function(){
			// nav.style.left = "0px";
			nav.style.left = "-250px";
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
	setTimeout(menu,400) // I give the javascript the time to load the nav
	window.addEventListener("scroll", on_scroll);
});