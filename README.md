# Map the GLAM
Visualizing the contributions of cultural institutions in Wikimedia Projects.

## Installation
- Go to the project folder in your computer
	```
	$ cd < path_to_the_folder >
	```
- Install the bower dependencies
	```
	$ bower install
	```
- Run local server 
	```
	$ python -m SimpleHTTPServer 8000
	```
- Access the webpage at
	```
	http:localhost:8000 < path_to_the_folder >
	```

## This project uses:
-	[Bower](https://bower.io/)
-	[JQuery](https://jquery.com/)
-	[Neat](http://neat.bourbon.io/)

[comment]: <> "[D3](https://d3js.org/)"
[comment]: <> "[Handlebars](http://handlebarsjs.com/)"

### Bower (install and update packages)
-	cd < path_to_the_folder >
-	bower install < package_name >
-	bower update

### Neat 
- 	update sass file
-	build the css (cmd + alt + B in Sublime Text)