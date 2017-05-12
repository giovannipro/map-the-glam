var baseurl = window.location.href;
var container = "#timeline_uploads"
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

function timeline_uploads(){

	var window_w = $("body").outerWidth(),
		window_h = $(container).height();
		//console.log(window_h)

	var margin = {top: 10, right: 10, bottom: 20, left: 30},
		width = window_w - (margin.left + margin.right),
		height = window_h - (margin.top + margin.bottom);

	var interpolation = [
		"curveLinear",
		"curveStep",
		"curveStepBefore",
		"curveStepAfter",
		"curveBasis",
		"curveCardinal",
		"curveMonotoneX",
		"curveCatmullRom"
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
		"easeBack"
	];

	function render(){
		var svg = d3.select(container)
			.append("svg")
			.attr("id", "svg")
			.attr("width", width + (margin.left + margin.right))
			.attr("height",height + (margin.top + margin.bottom))
			//.attr("viewBox", "0 0 " + width + " " + (height))

		var plot = svg.append("g")
			.attr("id", "d3_plot")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

		d3.tsv("assets/data/timeline_uploads.tsv", function (error, data) {
			if (error) throw error;

			var parseTime = d3.timeParse("%Y-%m");

			data.forEach(function (d) {
				d.date = parseTime(d.date);
				d.files = +d.files;
			})
			//console.log(data)

			// scale
			var x = d3.scaleTime().range([0, width]);
			var y = d3.scaleLinear().range([height, 0]);

			// domain
			x.domain(d3.extent(data, function(d) { return d.date; }));
			y.domain([0, d3.max(data, function(d) { return d.files; })]);

			var area_0 = d3.line()
				.curve(d3.curveStep)
				.x(function(d) { return x(d.date); })
				.y(function(d) { return y(0); })

			var area = d3.line()
				.curve(d3.curveStep)
				.x(function(d) { return x(d.date); })
				.y(function(d) { return y(d.files); })

			plot.append("path")
				.data([data])
				.attr("class", "uploads")
				.attr("d", area_0)
				.transition()
				//.ease("easeBounce")
				.delay(0)
				.duration(390)
				.attr("d", area);

			// axis
			var xAxis = plot.append("g")
				.attr("transform", "translate(0," + height + ")")
				.call(d3.axisBottom(x));

			var yAxis = plot.append("g")
				.call(d3.axisLeft(y));
		})
	}
	render();
}

function resize_dv(){
  	var window_w = $("body").outerWidth(),
	  	window_h = $(container).height();
	console.log(window_w)

	var margin = {top: 10, right: 10, bottom: 20, left: 30},
		width = window_w - (margin.left + margin.right),
		height = window_h - (margin.top + margin.bottom);

	var x = d3.scaleTime().range([0, width]);
	var y = d3.scaleLinear().range([height, 0]);

	svg.selectAll('.uploads')
		.attr("d", function(d) {
			return area(d);
		})
}

function open_docu(){
	var transition = 300;
	var my_class = "open_panel";
	var invisible = "invisible"

	function open_protocol(){
		$("#timeline_uploads_protocol").show() //.toggleClass("invisible",transition)
		$("#timeline_uploads_data").hide()
	}
	function open_data(){
		$("#timeline_uploads_data").show()  //.toggleClass("invisible",transition)
		$("#timeline_uploads_protocol").hide()
	}

	$("#timeline_uploads_open_protocol").click(function(){
		$("#timeline_uploads_open_data").removeClass("selected")
		$("#timeline_uploads_open_protocol").addClass("selected")

		if ($("#timeline_uploads_docu_container").hasClass("open_panel")) {
			if ($("#timeline_uploads_data").is(":visible")) {
				$("#timeline_uploads_protocol").show()
				$("#timeline_uploads_data").hide()
			}
			else {
				$("#timeline_uploads_open_protocol").removeClass("selected")
				$("#timeline_uploads_protocol").show()
				$("#timeline_uploads_docu_container").removeClass("open_panel")
			}
		}
		else {
			setTimeout(open_protocol,transition)
			$("#timeline_uploads_docu_container").addClass("open_panel")
		}
	})

	$("#timeline_uploads_open_data").click(function(){
		$("#timeline_uploads_open_protocol").removeClass("selected")
		$("#timeline_uploads_open_data").addClass("selected")

		if ($("#timeline_uploads_docu_container").hasClass("open_panel")) {
			if ($("#timeline_uploads_protocol").is(":visible")) {
				$("#timeline_uploads_data").show()
				$("#timeline_uploads_protocol").hide()
			}
			else {
				$("#timeline_uploads_open_data").removeClass("selected")
				$("#timeline_uploads_data").show()
				$("#timeline_uploads_docu_container").removeClass("open_panel")
			}
		}
		else {
			setTimeout(open_data,transition)
			$("#timeline_uploads_docu_container").addClass("open_panel")
		}	
	})
}

$( document ).ready(function() {
	header();
	footer();
	window.addEventListener("scroll", on_scroll);

	timeline_uploads();
	open_docu();
});


