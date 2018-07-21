function size(){
	// console.log("button")

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