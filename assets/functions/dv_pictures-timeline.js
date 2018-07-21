function pictures_timeline(){
	// console.log("pictures_timeline")
	var container = "#dv_pictures_timeline";
	
	var window_w = $("body").outerWidth(),
		window_h = $(container).height();

	var margin = {top: 10, right: 0, bottom: 0, left: 0},
		width = window_w - (margin.left + margin.right),
		height = window_h - (margin.top + margin.bottom);

	var transition = 500;

	function render(width){
		var svg = d3.select(container)
			.append("svg")
			.attr("id", "svg_pictures_timeline")
			.attr("width", window_w) //  + (margin.left + margin.right))
			.attr("height",height + (margin.top + margin.bottom))

		var plot = svg.append("g")
			.attr("class", "d3_plot")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

		d3.tsv("assets/data/pictures_timeline.tsv", function (error, data) {
			if (error) throw error;
			
			data.forEach(function (d) {
				d.files = +d.files;
			})
			console.log(data)

			var x_scale = d3.scaleOrdinal()
				.domain(data)
        		.range([0, width])

			var yMin = d3.min(data, function (d) {
				return d.files
			})

			var yMax = d3.max(data, function (d) {
				return d.files
			})
			console.log(yMax)

			var y_scale = d3.scaleLog() // scaleLinear
				.domain([(yMin+0.5), yMax])
				.range([height,0]);

        	var bar_width = width/data.length;
        	// console.log(bar_width) 

        	var chart = plot.append("g")

			var bar = chart.selectAll("bar")
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
					return height - y_scale(d.files)
				})

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
}