var container_analogic = "#dv_size_analogic";
	container_digital = "#dv_size_digital";
	mobile_w = 425,
	tablet_w = 768;
	window_w = $("body").outerWidth(),
	window_h = $(container_analogic).height();

function size(){
	// console.log("button")

	function buttons(){
		var original_button = $("#original_size_button")
		var digital_button = $("#digital_size_button")

		var original = $("#dv_size_analogic")
		var digital = $("#dv_size_digital")

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
		// console.log(width)

		var margin = {top: 0, right: 0, bottom: 0, left: 0},
			width = window_w - (margin.left + margin.right),
			height = width // window_h - (margin.top + margin.bottom);

		var transition = 500;

		// analogic
		var svg_analogic = d3.select(container_analogic)
			.append("svg")
			.attr("id", "svg_size_analogic")
			.attr("width", width) //  + (margin.left + margin.right))
			.attr("height",height + (margin.top + margin.bottom))

		var plot_analogic = svg_analogic.append("g")
			.attr("class", "d3_plot")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

		// digital
		var svg_digital = d3.select(container_digital)
			.append("svg")
			.attr("id", "svg_size_digital")
			.attr("width", width) //  + (margin.left + margin.right))
			.attr("height",height + (margin.top + margin.bottom))

		var plot_digital = svg_digital.append("g")
			.attr("class", "d3_plot")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

		// var chart_shift = {top: 20, right: 20, bottom: 20, left: 20};
		// 	chart_width = width - (chart_shift.left+chart_shift.right)
		// 	chart_height = height - (chart_shift.top+chart_shift.bottom)

		function render_blocks_digital(){
			d3.tsv("assets/data/digital_size_heatmap.tsv", function (error, data) {
				if (error) throw error;
				// console.log(width)
				
				data.forEach(function (d) {
					d.x = +d.x;
					d.y = +d.y;
					d.count = +d.count;
				})
				// console.log(data)

	        	var countMin = d3.min(data, function (d) {
					return d.count
				})
				var countMax = d3.max(data, function (d) {
					return d.count
				})
	        	var scale_count_blocks = d3.scaleLog() // scaleLinear scaleLog
					.domain([countMin, countMax])
	        		.range([0.01, 1])

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

				var chart = plot_digital.append("g")
					.attr("class", "chart")

        		// tooltip
				var tip = d3.tip()
					.attr("class", "d3-tip")
					.offset([-10, 0])
					.html(function(d) { 
						if (d.count > 1) {
							return d.count + " pictures"
						}
						else {
							return d.count + " picture"
						}
						
					});
				chart.call(tip)

				var grid = 23,
					grid_size = width/grid;
				var blocks = chart.selectAll("blocks")
	        		.data(data)
	        		.enter()
	        		.append("rect")
	        		.attr("transform",function(d,i){
	        			return "translate(" + x_scale(d.x) + "," + y_scale(d.y) + ")"
	        		})
	        		.attr("width",function(d,i){
	        			return grid_size
	        		})
	        		.attr("height",function(d,i){
	        			return grid_size
	        		})
	        		.attr("class",function(d,i){
	        			return "block " + d.count
	        		})
	        		.attr("opacity",function(d,i){
	        			return scale_count_blocks(d.count)
	        		})
	        		.attr("fill", colors.item_b)
	        		.on("mouseover", tip.show)
					.on("mouseout", tip.hide) 

				// axis
				var axis = plot_digital.append("g")
					.attr("class","axis")

				var xAxis = axis.append("g")
					.attr("transform", "translate(" + 0 + "," + (height-grid_size) + ")")
					.attr("class","xAxis")
					.attr("fill", colors.myAxis)
					// .transition()
					// .delay(transition)
					.call(d3.axisBottom(x_scale)
						// .tickFormat(d3.timeFormat("%m.%y")) //.every(o_ticks)) //d3.timeMonth.every(o_ticks))
						.tickSize(5)
						.ticks(20)
						.tickPadding(5)
						// .tickValues(
						// 	x_scale.domain().filter(function(d, i) { 
						// 		return i <= 10
						// 		// return !(i % o_ticks) && !(i==data.length-1) && !(i==data.length-2) //|| (i!=data.length-2)
						// 	})
						// )
					);

				var yAxis = axis.append("g")
					.attr("transform", "translate(25,0)")
					.attr("class","xAxis")
					.attr("fill", colors.myAxis)
					// .transition()
					// .delay(transition)
					.call(d3.axisLeft(y_scale)
						// .tickFormat(d3.timeFormat("%m.%y")) //.every(o_ticks)) //d3.timeMonth.every(o_ticks))
						.tickSize(5)
						.ticks(20)
						.tickPadding(5)
						// .tickValues(
						// 	x_scale.domain().filter(function(d, i) { 
						// 		return i <= 10
						// 		// return !(i % o_ticks) && !(i==data.length-1) && !(i==data.length-2) //|| (i!=data.length-2)
						// 	})
						// )
					);
	        })
		}
		render_blocks_digital();

		function render_blocks_analogic(){
			d3.tsv("assets/data/original_size_heatmap.tsv", function (error, data) {
				if (error) throw error;
				
				data.forEach(function (d) {
					d.x = +d.x;
					d.y = +d.y;
					d.count = +d.count;
				})
				// console.log(data)

	        	var countMin = d3.min(data, function (d) {
					return d.count
				})
				var countMax = d3.max(data, function (d) {
					return d.count
				})
				// console.log(countMin,countMax)
	        	var scale_count_blocks = d3.scaleLog() // scaleLinear scaleLog
					.domain([countMin, countMax])
	        		.range([0.01, 1])

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

				var grid = 31,
					grid_size = width/grid;
				var x_scale = d3.scaleLinear()
					.domain([0, max_max])
	        		.range([0, (width-grid_size)])
	        	var y_scale = d3.scaleLinear()
					.domain([max_max,0])
	        		.range([0,(height-grid_size)])

				var chart = plot_analogic.append("g")
					.attr("class", "chart")

        		// tooltip
				var tip = d3.tip()
					.attr("class", "d3-tip")
					.offset([-10, 0])
					.html(function(d) { 
						if (d.count > 1) {
							return d.count + " pictures"
						}
						else {
							return d.count + " picture"
						}
						
					});
				chart.call(tip)

				var blocks = chart.selectAll("blocks")
	        		.data(data)
	        		.enter()
	        		.append("rect")
	        		.attr("transform",function(d,i){
	        			return "translate(" + x_scale(d.x) + "," + y_scale(d.y) + ")"
	        		})
	        		.attr("width",function(d,i){
	        			return height/grid
	        		})
	        		.attr("height",function(d,i){
	        			return width/grid
	        		})
	        		.attr("class",function(d,i){
	        			return "block " + d.x + " " + d.y + " " + d.count
	        		})
	        		.attr("opacity",function(d,i){
	        			return scale_count_blocks(d.count)
	        		})
	        		.attr("fill", colors.item_b)
	        		.on("mouseover", tip.show)
					.on("mouseout", tip.hide) 

				// axis
				var axis = plot_analogic.append("g")
					.attr("class","axis")

				var xAxis = axis.append("g")
					.attr("transform", "translate(" + 0 + "," + (height-grid_size) + ")")
					.attr("class","xAxis")
					.attr("fill", colors.myAxis)
					// .transition()
					// .delay(transition)
					.call(d3.axisBottom(x_scale)
						// .tickFormat(d3.timeFormat("%m.%y")) //.every(o_ticks)) //d3.timeMonth.every(o_ticks))
						.tickSize(5)
						.ticks(20)
						.tickPadding(5)
						// .tickValues(
						// 	x_scale.domain().filter(function(d, i) { 
						// 		return i <= 10
						// 		// return !(i % o_ticks) && !(i==data.length-1) && !(i==data.length-2) //|| (i!=data.length-2)
						// 	})
						// )
					);

				var yAxis = axis.append("g")
					.attr("transform", "translate(25,0)")
					.attr("class","xAxis")
					.attr("fill", colors.myAxis)
					// .transition()
					// .delay(transition)
					.call(d3.axisLeft(y_scale)
						// .tickFormat(d3.timeFormat("%m.%y")) //.every(o_ticks)) //d3.timeMonth.every(o_ticks))
						.tickSize(5)
						.ticks(20)
						.tickPadding(5)
						// .tickValues(
						// 	x_scale.domain().filter(function(d, i) { 
						// 		return i <= 10
						// 		// return !(i % o_ticks) && !(i==data.length-1) && !(i==data.length-2) //|| (i!=data.length-2)
						// 	})
						// )
					);

	        })
		}
		render_blocks_analogic();

		/*function render_bubbles(){
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
	        		.attr("fill", "red")
	        })
	    }
	    // render_bubbles();*/
	}
	render_size(window_w)

	// function resize(){

	// 	$("#dv_size_analogic").remove()
	// 	$("#dv_size_digital").remove()

	// 	size(width);
	// }
	// window.addEventListener("resize", resize);


}