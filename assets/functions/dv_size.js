var container_analog = "#dv_size_analog";
	mobile_w = 425,
	tablet_w = 768;
	window_w = $("body").outerWidth(),
	window_h = $(container_analog).height();

function size(){
	// console.log("button")

	function buttons(){
		var original_button = $("#original_size_button")
		var digital_button = $("#digital_size_button")

		var original = $("#original_size")
		var digital = $("#digital_size")

		original_button.click(function(){
			//console.log("original")
			//this.css("font-weight","bold")
			original.show()
			digital.hide()
		})
		digital_button.click(function(){
			//console.log("digital")
			digital.show()
			original.hide()
		})
	}
	buttons();

	function render_size(width){

		var margin = {top: 0, right: 0, bottom: 0, left: 0},
			width = window_w - (margin.left + margin.right),
			height = width // window_h - (margin.top + margin.bottom);

		var transition = 500;

		var svg = d3.select(container_analog)
			.append("svg")
			.attr("id", "svg_size_analog")
			.attr("width", width) //  + (margin.left + margin.right))
			.attr("height",height + (margin.top + margin.bottom))

		var plot = svg.append("g")
			.attr("class", "d3_plot")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

		// var chart_shift = {top: 20, right: 20, bottom: 20, left: 20};
		// 	chart_width = width - (chart_shift.left+chart_shift.right)
		// 	chart_height = height - (chart_shift.top+chart_shift.bottom)

		function render_blocks(){
			d3.tsv("assets/data/digital_size_heatmap.tsv", function (error, data) {
				if (error) throw error;
				
				data.forEach(function (d) {
					d.x = +d.x;
					d.y = +d.y;
					d.count = +d.count;
				})
				console.log(data)

	        	var countMin = d3.min(data, function (d) {
					return d.count
				})
				var countMax = d3.max(data, function (d) {
					return d.count
				})
	        	var scale_count_blocks = d3.scaleLinear()
					.domain([countMin, countMax])
	        		.range([0.05, 1])

				var xMax = d3.max(data, function (d) {
					return d.x
				})
				var yMax = d3.max(data, function (d) {
					return d.y
				})

				if (xMax > yMax){
					var max_max = xMax
				}
				else {
					var max_max = yMax
				}

				var x_scale = d3.scaleLinear()
					.domain([0, max_max])
	        		.range([0, width])
	        	var y_scale = d3.scaleLinear()
					.domain([max_max,0])
	        		.range([0,height])

				var chart = plot.append("g")
					.attr("class", "chart")

				var blocks = chart.selectAll("blocks")
	        		.data(data)
	        		.enter()
	        		.append("rect")
	        		.attr("transform",function(d,i){
	        			return "translate(" + x_scale(d.x) + "," + y_scale(d.y) + ")"
	        		})
	        		.attr("width",function(d,i){
	        			return height/23
	        		})
	        		.attr("height",function(d,i){
	        			return width/23
	        		})
	        		.attr("class","blocks")
	        		.attr("opacity",function(d,i){
	        			return scale_count_blocks(d.count)
	        		})
	        		.attr("fill", colors.item_b)
	        })
		}
		render_blocks();

		function render_bubbles(){
	        d3.tsv("assets/data/digital_size.tsv", function (error, data) {
				if (error) throw error;
				
				data.forEach(function (d) {
					d.width_ = +d.width;
					d.height_ = +d.height;
					d.count = +d.count;
				})
				console.log(data)

				// dots
				var chart = plot.append("g")
	        		.attr("class","bubbles")
	        		// .attr("transform", function(d,i){ 
	        		// 	return "translate(" + chart_shift.left + "," + chart_shift.top + ")"
	        		// });

	        	var countMin = d3.min(data, function (d) {
					return d.count
				})
				var countMax = d3.max(data, function (d) {
					return d.count
				})
	        	var scale_count_blocks = d3.scaleLinear()
					.domain([countMin, countMax])
	        		.range([0.15, 1])

	        	var xMax = d3.max(data, function (d) {
					return d.width_
				})
				var yMax = d3.max(data, function (d) {
					return d.height_
				})

	        	var scale_count_bubbles = d3.scaleLinear()
					.domain([countMin, countMax])
	        		.range([5, 20])

	        	var x_scale = d3.scaleLinear()
					.domain([0, xMax])
	        		.range([0, width])

	        	var y_scale = d3.scaleLinear()
					.domain([yMax,0])
	        		.range([0,height])
		
				var bubbles = chart.selectAll("bubble")
	        		.data(data)
	        		.enter()
	        		.append("circle")
	        		.attr("transform",function(d,i){
	        			return "translate(" + x_scale(d.x) + "," + y_scale(d.y) + ")"
	        		})
	        		.attr("r",function(d,i){
	        			return scale_count_bubbles(d.count)
	        		})
	        		.attr("class","bubble")
	        		.attr("opacity",0.5)
	        		.attr("fill", "red") //colors.item_b*/
	        })
	    }
	    // render_bubbles();
	}
	render_size(window_w)

}