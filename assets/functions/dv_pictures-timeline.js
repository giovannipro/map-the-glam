var container = "#dv_pictures_timeline";

function pictures_timeline(){
	// console.log("pictures_timeline")
	
	var window_w = $("body").outerWidth(),
		window_h = $(container).height();

	var margin = {top: 0, right: 0, bottom: 0, left: 0},
		width = window_w - (margin.left + margin.right),
		height = window_h - (margin.top + margin.bottom);

	var transition = 500;

	function render(width){
		var svg = d3.select(container)
			.append("svg")
			.attr("id", "svg_pictures_timeline")
			.attr("width", width) //  + (margin.left + margin.right))
			.attr("height",height + (margin.top + margin.bottom))

		var plot = svg.append("g")
			.attr("class", "d3_plot")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

		var chart_shift = {top: 10, right: 10, bottom: 20, left: 55};
			chart_width = width - (chart_shift.left+chart_shift.right)
			chart_height = height - (chart_shift.top+chart_shift.bottom)

		d3.tsv("assets/data/pictures_timeline.tsv", function (error, data) {
			if (error) throw error;
			
			data.forEach(function (d) {
				d.files = +d.files;
			})
			// console.log(data)

			var x_scale = d3.scaleBand() //scaleOrdinal()
				.domain(data.map(function(d) { return d.decade})) // data
        		.range([0, chart_width])

			var yMin = d3.min(data, function (d) {
				return d.files
			})

			var yMax = d3.max(data, function (d) {
				return d.files
			})
			// console.log(yMax)

			var y_scale = d3.scaleLog() // scaleLinear
				.domain([(yMin+0.6), yMax])
				.range([chart_height,0]);

        	var bar_width = chart_width/data.length;
        	// console.log(bar_width) 

        	var chart = plot.append("g")
        		.attr("class","bars")
        		.attr("transform", "translate(" + chart_shift.left + "," + chart_shift.top + ")");

        	// bars
			var bars = chart.selectAll("bar")
				.data(data)
				.enter()
				.append("rect")
				.attr("class",function(d){
					return "bar " + d.decade + " " + d.files
				})
				.attr("x",function(d,i){
					return i*bar_width
				})
				.attr("y",function(d,i){
					return y_scale(d.files)
				})
				.attr("width",bar_width)
				.attr("height",function(d){
					return chart_height - y_scale(d.files)
				})
				.attr("fill",colors.item_b)

			// axis
			var axis = chart.append("g")
				.attr("class","axis")
				// .attr("transform", "translate(" + chart_shift.left + ",0)")

			// yAxis
			var yAxis = axis.append("g")
				.attr("class","yAxis")
				.attr("fill", colors.myAxis)
				.attr("transform", "translate(-5,0)")
				// .transition()
				// .delay(transition * 1.5)
				.call(d3.axisLeft(y_scale)
					.ticks(4)
					.tickFormat(d3.formatPrefix(",.0", 1)) // 1e3
				);

			// xAxis
			var mobile_w = 425,
				table_w = 768;
			if (width > table_w){
				o_ticks = 2
			}
			else if (width > mobile_w && width <= table_w) {
				o_ticks = 3
			}
			else {
				o_ticks = 5 // 6
			}

			var xAxis = axis.append("g")
				.attr("transform", "translate(" + 0 + "," + chart_height + ")")
				.attr("class","xAxis")
				.attr("fill", colors.myAxis)
				// .transition()
				// .delay(transition)
				.call(d3.axisBottom(x_scale)
					// .tickFormat(d3.timeFormat()).every(2) //.every(o_ticks)) //d3.timeMonth.every(o_ticks))
					.tickSize(0)
					// .ticks(o_ticks)
					.tickPadding(5)
					// .tickValues(x_scale.domain()
					.tickValues(
						x_scale.domain().filter(function(d, i) { 
							return !(i % o_ticks) && !(i==data.length-1) && !(i==data.length-2) //|| (i!=data.length-2)
							// return (d.decade == "uncertain") //|| (d.decade=="unknown"); 
						})
					)
				);

			function mouseover(){
				d3.select(this)
					.attr("opacity",0.4)
			}

			function mouseout(){
				d3.select(this)
					.attr("opacity",1)
			}

			d3.selectAll(".bar")
				.on("mouseover",mouseover)
			d3.selectAll(".bar")
				.on("mouseout",mouseout)
					
		})
	}
	render(width)

	function resize(){
		// var container = "#dv_pictures_timeline",
			width = $(container).outerWidth() - (margin.left + margin.right);
			console.log(width)
		$("#svg_pictures_timeline").remove()	

		render(width);
	}

	window.addEventListener("resize", resize);
}