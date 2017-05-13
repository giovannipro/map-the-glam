var baseurl = window.location.href;
var container = "#dv_timeline_uploads"
//var baseurl = document.location.origin;
//console.log(baseurl)

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
	var transition = 300;
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
		data_button.removeClass("selected")
		protocol_button.addClass("selected")

		if (docu_container.hasClass("open_panel")) {
			if (data.is(":visible")) {
				protocol.show()
				data.hide()
			}
			else {
				protocol_button.removeClass("selected")
				protocol.show()
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
				data.show()
				docu_container.removeClass("open_panel")
			}
		}
		else {
			setTimeout(open_data,transition)
			docu_container.addClass("open_panel")
		}	
	})
}

$( document ).ready(function() {
	header();
	footer();
	//dataviz_docu();
	window.addEventListener("scroll", on_scroll);

	open_docu("timeline_uploads");
	open_docu("category_network");
	open_docu("size");
	open_docu("spread");
	open_docu("lang");
	open_docu("page_views");
});


