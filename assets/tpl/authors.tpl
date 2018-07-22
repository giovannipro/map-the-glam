<ul class="authors_grid">
{{#each this}}
	<li class="author_box" style="height:{{author_bar pictures max_val max_height}}px;">
		<span class="author_name">{{author}}</span>
		<span class="n_pictures">{{pictures}}</span>
		{{!-- {{max_val}} {{max_height}} --}}
	</li>
{{/each}}
</ul>