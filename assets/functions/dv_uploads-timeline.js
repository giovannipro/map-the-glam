function uploads_timeline(){
	var container = "#dv_uploads_timeline";
	
	var window_w = $("body").outerWidth(),
		window_h = $(container).height();
		//console.log(window_h)

	var margin = {top: 10, right: 0, bottom: 20, left: 0},
		width = window_w - (margin.left + margin.right),
		height = window_h - (margin.top + margin.bottom);

	var ease = d3.easePoly;
	var interpolation = curve[5] //d3.curveMonotoneX;
	var transition = 500;

	function render(width){
		var svg = d3.select(container)
			.append("svg")
			.attr("id", "svg_uploads_timeline")
			.attr("width", width + (margin.left + margin.right))
			.attr("height",height + (margin.top + margin.bottom))

		var plot = svg.append("g")
			.attr("class", "d3_plot")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

		d3.tsv("assets/data/uploads_timeline.tsv", function (error, data) { // test timeline_uploads
			if (error) throw error;

			var parseTime = d3.timeParse("%Y-%m");
			data.forEach(function (d) {
				d.date = parseTime(d.date);
				d.cc_by_sa_4 = +d.cc_by_sa_4;
				d.cc_by_4 = +d.cc_by_4;
				d.public_domain = +d.public_domain;
			})
			// console.log(data)

			var stack = d3.stack()
				.keys(["cc_by_sa_4", "public_domain", "cc_by_4"])
				.order(d3.stackOrderAscending) // stackOrderNone stackOrderAscending 
				.offset(d3.stackOffsetNone); //  stackOffsetWiggle stackOffsetDiverging stackOffsetSilhouette stackOffsetNone

			var stack_data = stack(data);
			var data_length = data.length;
			// console.log(stack_data)

			var x_scale = d3.scaleTime()
				.domain(d3.extent(data, function(layer) { 
        			return layer.date;
        		}))
        		.range([0, width])
			
			var xMax = d3.max(data, function(d) { return d.date; })

			var bar_width = width/data_length
			var x_b = d3.scaleTime() // scaleLinear() scaleBand()
				.domain(d3.extent(data, function(layer) { 
        			return layer.date;
        		}))
    			// .domain([0, xMax])
				.range([(bar_width/2), width-(bar_width / 2)]) // .rangeRound([0, width])

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
				.range([height,0]);

			var z = d3.scaleOrdinal()
    			.range([
    				colors.item_a,
    				colors.item_b,
    				colors.item_c
    			])
    			.domain(data.columns.slice(1))

			// var area = d3.area()
			// 	.x(function(d, i) { return  x_scale(d.data.date) }) 
			// 	.y0(function(d) { return y_scale(d[0]) })
			// 	.y1(function(d) { return y_scale(d[1]) })//y_scale(d[1]) })
			// 	.curve (d3.curveBasis)

			var license_box = plot.append("g")
				.attr("class","legend")
				.selectAll("g")
				.data(stack_data)
				.enter()
				.append("g")
				.attr("class","path")
				.attr("id",function(d,i) { 
					return d.key
				})
				.attr("opacity",1)

			// var area_0 = d3.area()
			// 	.x(function(d, i) { return  x_scale(0) }) 
			// 	.y0(function(d) { return y_scale(0) })
			// 	.y1(function(d) { return y_scale(0) })

			// area
			/*license_box.append("path")
				.attr("d", area)
				.attr("fill", function(d,i) { 
					if (d.key == "public_domain"){
						return colors.a
					}
					else if (d.key == "cc_by_sa_4") {
						return colors.b
					}
					else {
						return colors.c
					}
				})*/

			// bars 
			// https://bl.ocks.org/mbostock/1134768
			// https://bl.ocks.org/mbostock/1134768
			// https://bl.ocks.org/mjfoster83/7c9bdfd714ab2f2e39dd5c09057a55a0

			var y_b = d3.scaleLinear()
				.domain([0,yMax])
				.rangeRound([height, 0]);

			var bars_group = plot.append("g")
				.attr("class","bars")
				// .attr("transform", function(d) { 
				// 	 return "translate(" + x_b(d.date) + "," + (height - y_b(d[0])) + ")"; 
			 //  	})

				
			// tooltip
			var tip = d3.tip()
				.attr("class", "d3-tip")
				.offset([-10, 0])
				.html(function(d) { 
					return "pd: " + d.pd
				});
			svg.call(tip)

			var bar = bars_group.selectAll("bars")
				.data(stack_data)
				.enter()
				.append("g")
				.attr("fill", function(d) { return z(d.key); })
				.selectAll("rect")
				.data(function(d) { return d; })
				.enter()
				.append("rect")
				.attr("width", bar_width) //  x_b.bandwidth
				.attr("height", function(d) {
					return y_b(d[0]) - y_b(d[1])
				})
				.attr("x", function(d,i) { return i*(width/data_length)  }) // x_b(d.date);
				.attr("y", function(d) { return y_b(d[1]) })
    //  			.on("mouseover", tip.show)
				// .on("mouseout", tip.hide) 
				
			var mobile_w = 425,
				table_w = 768;
			if (width > table_w){
				o_ticks = 15
			}
			else if (width > mobile_w && width <= table_w) {
				o_ticks = 8
			}
			else {
				o_ticks = 3 // 6
			}

			// axis
			var xAxis = plot.append("g")
				.attr("transform", "translate(" + 0 + "," + height + ")")
				.attr("class","xAxis")
				.attr("fill", colors.myAxis)
				// .transition()
				// .delay(transition)
				.call(d3.axisBottom(x_b)
					.tickFormat(d3.timeFormat("%m.%y")) //.every(o_ticks)) //d3.timeMonth.every(o_ticks))
					.tickSize(0)
					.ticks(o_ticks)
					.tickPadding(5)
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

			var highlight_box = svg.append("g")
				.attr("class","highlight")

			/*var highlight_line = highlight_box.append("line")
      			.attr("x1", -5)
				.attr("y1", 0)
				.attr("x2", -5)
				.attr("y2", window_h)
				.attr("stroke","red")
				.attr("id","line_timeline_uploads");*/

			var legend_box = highlight_box.append("g")
				.attr("transform","translate(10,30)")
				.attr("id","toltip_uploads_timeline")
				
			// legend_box.append("svg:tspan")
			legend_box.append("text")
				.attr("id","uploads_timeline_pd")

			legend_box.append("text")
				.attr("id","uploads_timeline_by")
				.attr("transform","translate(0,25)")

			legend_box.append("text")
				.attr("id","uploads_timeline_sa")
				.attr("transform","translate(0,50)")

			var highlight_rect = highlight_box.append("rect")
				.attr("x", -width/data_length)
            	.attr("y", 0)
            	.attr("width", bar_width)
                .attr("height", window_h)
           		.style("fill-opacity", 0.4)
           		.style("fill", "white")
           		.attr("id","highlightRect_uploads_timeline");

			var bisectDate = d3.bisector(function(d) { return d.date; }).left;
			
			function roundTo(n,round){
				// return Math.round(((n%round) > 0)?n-(n%round) + round:n);
				return ((n%round) > 0)?n-(n%round) + round:n;
			}

			function mousemove() {
				var mouse_x = d3.mouse(this)[0];
				var graph_x = x_scale.invert(mouse_x);
				var x0 = x_scale.invert(d3.mouse(this)[0]);
				i = bisectDate(data, x0, 1)
				d0 = data[i - 1],
      			d1 = data[i],
      			d = x0 - d0.date > d1.date - x0 ? d1 : d0;

      			// cc_sa = d["cc_by_sa_4"]
      			// cc_by = d["cc_by_4"]
      			// pd = d["public_domain"]

      			d3.select("#line_uploads_timeline")
      				.attr("x1", mouse_x)
					.attr("y1", 0)
					.attr("x2", mouse_x)
					.attr("y2", height)
					.attr("stroke","red");

				d3.select("#highlightRect_uploads_timeline")
					.attr("x", roundTo(mouse_x,bar_width)-bar_width)

				toltip_pd = "pd: " + pd
				toltip_by = "cc-by: " + cc_by
				toltip_sa = "cc-by-sa: " + cc_sa
					
				d3.select("#uploads_timeline_pd")
					.text(toltip_pd)

				d3.select("#uploads_timeline_by")
					.text(toltip_by)

				d3.select("#uploads_timeline_sa")
					.text(toltip_sa)
					.attr("transform","translate(20,30)")

				// console.log(mouse_x)
			}

			d3.select("#dv_uploads_timeline")
				.on("mousemove", mousemove);
		})
	}
	render(width);

	function resize(){
		var container = "#dv_uploads_timeline",
			width = $(container).outerWidth() - (margin.left + margin.right);
			// console.log(width)
		$("#svg_uploads_timeline").remove()	

		render(width);
	}

	window.addEventListener("resize", resize);
}