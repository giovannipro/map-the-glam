Handlebars.registerHelper("multiply", function(foo, bar){
  	var result =  foo * bar
	if ( (result - Math.floor(result)) !== 0 ){
		return (result).toFixed(1)
	}
	else {
		return result;
	}
});

Handlebars.registerHelper("author_bar", function(pic, max_pic, max_h){
	var result = (pic*max_h)/max_pic
		min_height = 7 // 10
	if (result < min_height) {
		return min_height
	}
	else {
		return result
	}
})