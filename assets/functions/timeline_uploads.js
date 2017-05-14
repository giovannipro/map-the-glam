function timeline_uploads(){

	var window_w = $("body").outerWidth(),
		window_h = $(container).height();
		//console.log(window_h)

	var margin = {top: 20, right: 30, bottom: 40, left: 50},
		width = window_w - (margin.left + margin.right),
		height = window_h - (margin.top + margin.bottom);

	var curve = [
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
		"easeBack",
		"easeExpOut",
		"easeExpInOut",
		"easeCircleOut"
	];

	var ease = d3.easePoly;
	var interpolation = d3.curveMonotoneX;
	var transition = 500;

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
				.curve(interpolation)
				.x(function(d) { return x(d.date); })
				.y(function(d) { return y(0); })

			var area = d3.line()
				.curve(interpolation)
				.x(function(d) { return x(d.date); })
				.y(function(d) { return y(d.files); })

			plot.append("path")
				.data([data])
				.attr("class", "uploads")
				.attr("d", area_0)
				.transition()
				.ease(ease)
				.delay(0)
				.duration(transition)
				.attr("d", area);

			o_ticks = 0

			if (window_w < 700) {
				o_ticks = 3
			}
			else{
				o_ticks = 20
			}

			// axis
			var xAxis = plot.append("g")
				.attr("transform", "translate(0," + (height + 5) + ")")
				.attr("class","xAxis")
				.transition()
				.delay(transition * 1.5)
				.call(d3.axisBottom(x)
					.ticks(o_ticks)
				);

			var yAxis = plot.append("g")
				.attr("class","yAxis")
				.attr("transform", "translate(-15,0)")
				.transition()
				.delay(transition * 1.5)
				.call(d3.axisLeft(y)
					.ticks(6)
					.tickFormat(d3.formatPrefix(",.0", 1e3))
				);
		})
	}
	render();
}

$( document ).ready(function() {
	timeline_uploads();
});