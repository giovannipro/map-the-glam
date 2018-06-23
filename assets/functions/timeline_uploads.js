var curve = [
	"d3.curveLinear",
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

function timeline_uploads(){

	var window_w = $("body").outerWidth(),
		window_h = $(container).height();
		//console.log(window_h)

	var margin = {top: 0, right: 0, bottom: 10, left: 0},
		width = window_w - (margin.left + margin.right),
		height = window_h - (margin.top + margin.bottom);

	var ease = d3.easePoly;
	var interpolation = d3.curveMonotoneX;
	var transition = 500;

	function render(width){
		var svg = d3.select(container)
			.append("svg")
			.attr("id", "svg_timeline_uploads")
			.attr("width", width + (margin.left + margin.right))
			.attr("height",height + (margin.top + margin.bottom))

		var plot = svg.append("g")
			.attr("class", "d3_plot")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

		d3.tsv("assets/data/timeline_uploads.tsv", function (error, data) { // timeline_uploads_test
			if (error) throw error;

			var parseTime = d3.timeParse("%Y-%m");
			data.forEach(function (d) {
				d.date = parseTime(d.date);
				d.cc_by_sa_4 = +d.cc_by_sa_4;
				d.public_domain = +d.public_domain;
			})
			// console.log(data)

			var stack = d3.stack()
				.keys(["cc_by_sa_4", "public_domain", "cc_by_4"])
				.order(d3.stackOrderAscending) // stackOrderNone stackOrderAscending 
				.offset(d3.stackOffsetNone); //  stackOffsetWiggle stackOffsetDiverging stackOffsetSilhouette stackOffsetNone

			var stack_data = stack(data);
			// console.log(stack_data)

			var x_scale = d3.scaleTime()
				.domain(d3.extent(data, function(layer) { 
        			return layer.date;
        		}))
        		.range([0, width])

			var yMin = d3.min(stack_data, function (layer) {
				return d3.min(layer, function(d){ 
					return d[0]
				})
			})

			var yMax = d3.max(stack_data, function (layer) {
				return d3.max(layer, function(d){ 
					return d[1]
				})
			})
			
			var y_scale = d3.scaleLinear()
				.domain([yMin, yMax])
				.range([(height-30),0]);

			var area = d3.area()
				.x(function(d, i) { return  x_scale(d.data.date) }) 
				.y0(function(d) { return y_scale(d[0]) })
				.y1(function(d) { return y_scale(d[1]) })
				// .curve(curve[6].d3Curve);
				.curve (d3.curveBasis)

			var license_box = plot.selectAll("g")
				.data(stack_data)
				.enter()
				.append("g")
				.attr("class","path")
				.attr("id",function(d,i) { 
					return d.key
				})

			license_box.append("path")
				.attr("d", area)
				.attr("fill", function(d,i) { 
					if (d.key == "public_domain"){
						return "red"
					}
					else if (d.key == "cc_by_sa_4") {
						return "blue"
					}
					else {
						return "green"
					}
				})

			o_ticks = 0
			if (width < 700) {
				o_ticks = 6
			}
			else{
				o_ticks = 20
			}

			// axis
			var xAxis = plot.append("g")
				.attr("transform", "translate(0," + (height-20) + ")")
				.attr("class","xAxis")
				// .transition()
				// .delay(transition * 1.5)
				.call(d3.axisBottom(x_scale)
					.ticks(o_ticks)
				);

			// var yAxis = plot.append("g")
			// 	.attr("class","yAxis")
			// 	.attr("transform", "translate(-10,0)")
			// 	// .transition()
			// 	// .delay(transition * 1.5)
			// 	.call(d3.axisLeft(y_scale)
			// 		.ticks(6)
			// 		.tickFormat(d3.formatPrefix(",.0", 1e3))
			// 	);

			var line_box = d3.select("#svg_timeline_uploads")
				.append("g")
				.attr("class","line")

			line_box.append("line")
      			.attr("x1", -5)
				.attr("y1", 0)
				.attr("x2", -5)
				.attr("y2", window_h)
				.attr("stroke","red")
				.attr("id","line_timeline_uploads");

			line_box.append("text")
				.text("a")
				.attr("id","toltip_timeline_uploads")

			var bisectDate = d3.bisector(function(d) { return d.date; }).left;

			function mousemove() {
				var mouse_x = d3.mouse(this)[0];
				var graph_x = x_scale.invert(mouse_x);
				var x0 = x_scale.invert(d3.mouse(this)[0]);
				i = bisectDate(data, x0, 1)
				d0 = data[i - 1],
      			d1 = data[i],
      			d = x0 - d0.date > d1.date - x0 ? d1 : d0;

      			cc = d["cc_by_sa_4"]
      			pd = d["public_domain"]
      			// console.log(d, /*mouse_x, cc, pd*/)

      			d3.select("#line_timeline_uploads")
      				.attr("x1", mouse_x)
					.attr("y1", 0)
					.attr("x2", mouse_x)
					.attr("y2", height + margin.top + margin.bottom)
					.attr("stroke","red");

				toltip = "cc: " + cc + " pd: " + pd

				d3.select("#toltip_timeline_uploads")
					.text(toltip)
					.attr("transform","translate(20,30)")

				// line_box.textContent = "aa"

			}

			d3.select('svg')
				.on('mousemove', mousemove);

		})
	}
	render(width);

	function resize(){
		var container = "#dv_timeline_uploads",
			width = $(container).outerWidth() - (margin.left + margin.right);
		
		$("#svg_timeline_uploads").remove()	

		render(width);
	}

	window.addEventListener("resize", resize);
}

$( document ).ready(function() {
	timeline_uploads();
});