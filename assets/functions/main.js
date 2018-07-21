$( document ).ready(function() {
	header();
	footer();
	
	uploads_timeline();
	pictures_timeline();
	size();

	open_docu("glam_map");
	open_docu("timeline_uploads");
	open_docu("category_network");
	open_docu("size");
	open_docu("spread");
	open_docu("lang");
	open_docu("page_views");

	loading_time = new Date() - start;
	page_size(loading_time);
});

// console.timeEnd()
