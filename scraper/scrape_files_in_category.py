#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Get files in category

import os							# get file path
import sys							# reset file encoding
import webbrowser					# open webpages
import urllib, json, io				# read json
from urllib import urlopen			# open file

reload(sys)
sys.setdefaultencoding("utf-8")

# -----------------------------------
# Utilities

folder = os.path.dirname(os.path.realpath(__file__))
t = "\t"
n = "\n"
s = " "

# -----------------------------------
# Main variables

commons_api = "https://commons.wikimedia.org/w/api.php?action=query&format=json&list=categorymembers&cmtitle=Category:"
limit = 500
cont = 0

# -----------------------------------
# Script

def get_files(category,cont):

	f_out = folder + "/" + str(category) + ".tsv"

	if cont == 0:
		request = commons_api + category + "&cmlimit=" + str(limit)
	else:
		request = commons_api + category + "&cmlimit=" + str(limit) + "&cmcontinue=" + str(cont)

	response = urlopen(request).read()
	data = json.loads(response)

	with open(f_out, "a") as f:
		
		for x in data["query"]["categorymembers"]:

			try: 
				title = x["title"];
				output = title + n

				f.write(output)
				#print(data)
			except:
				pass

		new_new_cont = data["continue"]["cmcontinue"]
		#print(cont)
		#print(new_cont)

		index = 0

		if (new_new_cont != 0 and new_new_cont != cont): 
			get_files(category,new_new_cont)
			index += 1
			print("continue")
		else:
			print("stop")

def get_first_files(category):

	f_out = folder + "/" + str(category) + ".tsv"
	request = commons_api + category + "&cmlimit=" + str(limit)

	response = urlopen(request).read()
	data = json.loads(response)
	print(request)

	with open(f_out, "a") as f:
		
		for x in data["query"]["categorymembers"]:

			title = x["title"];
			output = title + n

			f.write(output)
			#print(data)

		new_cont = data["continue"]["cmcontinue"]
		#print(cont)
		#print(new_cont)

		index = 0

		if (new_cont != 0): 
			get_files(category,new_cont)
			index += 1
			print("continue")
		# else:
		# 	print("stop")

def loop(x):
		
	index = 0

	while index < x:
		index += 1
		print(index)

def inloop(x):
	print (x)

	index = x

	if index < x:
		index -= 1
		inloop(index)

# -----------------------------------
# Launch scripts

get_files("Media_contributed_by_the_Swiss_Federal_Archives",0)
