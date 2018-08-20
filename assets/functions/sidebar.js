function truncate(string){
	var max_size = 60;
   	if (string.length > max_size){
   		var extension = string.split(".").pop(-1);
   		return string.substring(0,max_size) + ' … .' + extension;
    }
	else{
		return string;
	}
};

function sidebar(data_file,title){
	// console.log("sidebar");

	var container = $("#sidebar"),
		header = $("#sidebar_header"),
		list = $("#files_list")
		overlay = $("#overlay");
	
	header.empty();
	list.empty();

	container.css("right",0);
	header.css({"position":"fixed"}); // ,"width":"432px"
	$("body").css("overflow","hidden");
	// overlay.css({"width":"100%","height":"100vh"})
	overlay.show();

	var close_btn = "<span class='closebtn' id='close_sidebar'>x</span>",
		header_box = "<span>" + title + "</span>";
	header.html(header_box + close_btn);

	var tpl = "assets/tpl/files.tpl";
		data_source = data_file;
	
	// function closeNav() {
	$("#close_sidebar").on("click", function() {
		container.css("right","-480px");
		$("body").css("overflow","visible");
		overlay.hide();
	})

	$("#overlay").on("click", function() {
		container.css("right","-480px");
		$("body").css("overflow","visible");
		overlay.hide();
	})

	$.get(tpl, function(tpl) {
		$.getJSON(data_source, function(data) {
			var template = Handlebars.compile(tpl);

			sorted_data = data.sort(function (a, b) {
				return b.file - a.file;
			})

			$.each(sorted_data, function(i,v){
				v["file_short"] = truncate(v.file)
			})
			// console.log(sorted_data)

			$(list).html(template(sorted_data));


		})
	})
}