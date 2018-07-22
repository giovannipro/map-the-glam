<ul class="authors_grid">
{{#each this}}
	<li class="author_box" style="height:{{author_bar pictures max_val max_height}}px;">
		{{author}} ({{pictures}})
		{{!-- {{max_val}} {{max_height}} --}}
	</li>
{{/each}}
</ul>