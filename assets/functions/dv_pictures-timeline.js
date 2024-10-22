var container = "#dv_pictures_timeline";
	mobile_w = 425,
	tablet_w = 768;

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

		var chart_shift = {top: 30, right: 10, bottom: 20, left: 55};
			chart_width = width - (chart_shift.left+chart_shift.right)
			chart_height = height - (chart_shift.top+chart_shift.bottom)

		d3.tsv("assets/data/pictures_timeline.tsv", function (error, data) {
			if (error) throw error;
			
			data.forEach(function (d) {
				d.files = +d.files;
				// if (d.files==0){
				// 	return 0.6
				// }
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
					return "bar" // + d.files
				})
				.attr("id",function(d){
					return d.decade
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
				.attr("fill","#9fcdde") //colors.item_c)

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
			if (width > tablet_w){
				o_ticks = 2
			}
			else if (width > mobile_w && width <= tablet_w) {
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
					// .attr("opacity",0.4)
					.attr("fill",colors.item_b)
			}

			function mouseout(){
				d3.select(this)
					.attr("fill","#9fcdde")
					// .attr("opacity",1)
			}

			d3.selectAll(".bar")
				.on("mouseover",mouseover)
			d3.selectAll(".bar")
				.on("mouseout",mouseout)
		})
	}
	render(width);

	function authors_chart(){
		var target = $("#authors_box"),
			tpl = "assets/tpl/authors.tpl";
			data_source_start = "assets/data/authors/authors_all.json";
			target_height = ($("#authors").height() - 300); // 

			if (width > tablet_w){
				target_height = target_height
			}
			else if (width > mobile_w && width <= tablet_w) {
				target_height = target_height/1.5
			}
			else {
				target_height = target_height/3
			}
			// console.log(target_height)

		function isotope(){
			$(".authors_grid").isotope({
				itemSelector: ".author_box",
				layoutMode: "packery", //"packery",
				percentPosition: true,
				packery: {
					gutter: 5 //, ".gutter-sizer",
					// columnWidth: ".grid-sizer"
				},
				// sortBy: pictures
				// masonry: {
				// 	gutter: 15, // space between blocks
				// 	horizontalOrder: true,
				// 	// fitWidth: true
				// }
			});
		};

		// function load_data(id){
		// 	// console.log(id)
		// 	$.get(tpl, function(tpl) {

		// 	 	my_id = ""
		// 	 	if (id == "all"){
		// 	 		my_id = "all authors"
		// 	 	}
		// 	 	else {
		// 	 		my_id = id
		// 	 	}

		// 	 	var id_box = "<div class='decade_box'><h4>" + my_id + "</h4><h5 id='all_authors' style='text-decoration: underline; cursor:pointer;'>(see all)</h5"
			 
		// 	 	var data_source = "assets/data/authors/authors_" + id + ".json";

		// 	 	// $("#authors_box").empty();
		// 	 	$("#decade_box").empty();

		// 	 	$.getJSON(data_source, function(data) {
		// 			var template = Handlebars.compile(tpl);
		// 				sorted_data = data.sort(function (a, b) {
		// 					return b.pictures - a.pictures;
		// 				})
		// 				// console.log(sorted_data)

		// 				var max = 0;                
		// 				$.map(data, function (obj) {
		// 					if (obj.pictures > max){
		// 				  		max = obj.pictures;
		// 					}
		// 				});

		// 				$.each(data, function(i,v){
		// 					v["max_val"] = max;
		// 					v["max_height"] = target_height;
		// 				})
						
		// 			$("#decade_box").html(id_box);
		// 			$(target).html(template(sorted_data));

		// 			isotope();
		// 		})


		// 	})
		// }
		// load_data("all");	

		// first load
		$.get(tpl, function(tpl) {

			// $(".bar").click(function() {
			 	var id = $(this).attr("id");

			 	my_id = ""
			 	if (id == "all"){
			 		my_id = "all authors"
			 	}
			 	else if (id == undefined){
			 		my_id = "all authors 1550-2009"
			 	}
			 	else {
			 		my_id = id
			 	}

			 	var id_box = "<div class='decade_box'><h4>" + my_id + "</h4><h5 id='all_authors' style='text-decoration: underline; cursor:pointer;'>(see all)</h5"
			 	
			 	target.empty();
			 	$("#decade_box").empty();

			 	$.getJSON(data_source_start, function(data) {
					var template = Handlebars.compile(tpl);
						sorted_data = data.sort(function (a, b) {
							return b.pictures - a.pictures;
						})
						// console.log(sorted_data)

						var max = 0;                
						$.map(data, function (obj) {
							// console.log(obj)
							if (obj.pictures > max){
						  		max = obj.pictures;
						  		// console.log(max)
							}
						});

						$.each(data, function(i,v){
							v["max_val"] = max;
							v["max_height"] = target_height;
						})
						
						// $("#decade_box").append(title);
						$("#decade_box").append(id_box);
						$(target).html(template(sorted_data));

						isotope();

						$("#all_authors").click(function() {
						 	data_source = "assets/data/authors/authors_" + "authors_all" + ".json";
						 	console.log(1)

						 	target.empty();
				 			$("#decade_box").empty();

				 			$.getJSON(data_source_start, function(data) {
								var template = Handlebars.compile(tpl);
									sorted_data = data.sort(function (a, b) {
										return b.pictures - a.pictures;
									})
									// console.log(sorted_data)

									var max = 0;                
									$.map(data, function (obj) {
										// console.log(obj)
										if (obj.pictures > max){
									  		max = obj.pictures;
									  		// console.log(max)
										}
									});

									$.each(data, function(i,v){
										v["max_val"] = max;
										v["max_height"] = target_height;
									})
									
								// $("#decade_box").append(title);
								$("#decade_box").append(id_box);
								$(target).html(template(sorted_data));

						isotope();
					})
				})
			})
		})

		//load by user (bars)
		$.get(tpl, function(tpl) {

			$(".bar").click(function() {
			 	var id = $(this).attr("id");
			 	data_source = "assets/data/authors/authors_" + id + ".json";

			 	my_id = ""
			 	if (id == "all"){
			 		my_id = "all authors"
			 	}
			 	else if (id == "uncertain"){
			 		my_id = "uncertain dates"
			 	}
			 	else if (id == "unknown"){
			 		my_id = "unknown dates"
			 	}
			 	else {
			 		my_id = id
			 	}

			 	var id_box = "<div class='decade_box'><h4>" + my_id + "</h4><h5 id='all_authors' style='text-decoration: underline; cursor:pointer;'>(see all)</h5"
			 	
			 	target.empty();
			 	$("#decade_box").empty();

			 	$.getJSON(data_source, function(data) {
					var template = Handlebars.compile(tpl);
						sorted_data = data.sort(function (a, b) {
							return b.pictures - a.pictures;
						})
						// console.log(sorted_data)

						var max = 0;                
						$.map(data, function (obj) {
							// console.log(obj)
							if (obj.pictures > max){
						  		max = obj.pictures;
						  		// console.log(max)
							}
						});

						$.each(data, function(i,v){
							v["max_val"] = max;
							v["max_height"] = target_height;
						})

					// $("#decade_box").append(title);
					$("#decade_box").append(id_box);
					$(target).html(template(sorted_data));

					isotope();

					$("#all_authors").click(function() {
					 	data_source = "assets/data/authors/authors_" + "authors_all" + ".json";
					 	// console.log(1)

					 	target.empty();
			 			$("#decade_box").empty();

			 			$.getJSON(data_source_start, function(data) {
							var template = Handlebars.compile(tpl);
								sorted_data = data.sort(function (a, b) {
									return b.pictures - a.pictures;
								})
								// console.log(sorted_data)

								var max = 0;                
								$.map(data, function (obj) {
									// console.log(obj)
									if (obj.pictures > max){
								  		max = obj.pictures;
								  		// console.log(max)
									}
								});

								$.each(data, function(i,v){
									v["max_val"] = max;
									v["max_height"] = target_height;
								})
								
							// $("#decade_box").append(title);
							$("#decade_box").append(id_box);
							$(target).html(template(sorted_data));

							isotope();
						})
					})
				})
			 })
		})

		// $("#all_authors").click(function() {
		// 	console.log(1)
		// })

		//load by user (see all)
		// $.get(tpl, function(tpl) {

			// $("#all_authors").on("click", function(){
			//  	data_source = "assets/data/authors/authors_" + authors_all + ".json";

			//  	console.log(1)

			 	// my_id = ""
			 	// if (id == "all"){
			 	// 	my_id = "all authors"
			 	// }
			 	// else {
			 	// 	my_id = id
			 	// }

			 	// var id_box = "<div class='decade_box'><h4>" + my_id + "</h4><h5 id='all_authors' style='text-decoration: underline; cursor:pointer;'>(see all)</h5"
			 	
			 	// target.empty();
			 	// $("#decade_box").empty();

			 	// $.getJSON(data_source, function(data) {
					// var template = Handlebars.compile(tpl);
					// 	sorted_data = data.sort(function (a, b) {
					// 		return b.pictures - a.pictures;
					// 	})

					// 	var max = 0;                
					// 	$.map(data, function (obj) {
					// 		if (obj.pictures > max){
					// 	  		max = obj.pictures;
					// 		}
					// 	});

					// 	$.each(data, function(i,v){
					// 		v["max_val"] = max;
					// 		v["max_height"] = target_height;
					// 	})

					// $("#decade_box").append(title);
					// $("#decade_box").append(id_box);
					// $(target).html(template(sorted_data));

					// isotope();
				// })
			 // })
		// })

		// function reload_data(){	
		// 	$(".bar").click(function() {
		// 		var id = $(this).attr("id");
		// 		console.log(id);
		// 		load_data(id);
		// 	})	
		// }	
		// reload_data()
	}
	authors_chart();
	
	function resize(){
		// var container = "#dv_pictures_timeline",
			width = $(container).outerWidth() - (margin.left + margin.right);
			// console.log(width)
		$("#svg_pictures_timeline").remove()	

		render(width);
		authors_chart();
	}
	window.addEventListener("resize", resize);

}