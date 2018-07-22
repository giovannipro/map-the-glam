$( document ).ready(function() {
	cookie_intro();

	// header();
	// footer();

	setTimeout(menu,400) // I give the javascript the time to load the nav
	window.addEventListener("scroll", on_scroll);

	goto_top();
	
	pictures_timeline();
	uploads_timeline();
	size();

	open_docu("pictures_timeline");
	open_docu("uploads_timeline");
	open_docu("category_network");
	open_docu("size");
	open_docu("spread");
	open_docu("lang");
	open_docu("page_views");

	loading_time = new Date() - start;
	page_size(loading_time);
});

// console.timeEnd()
