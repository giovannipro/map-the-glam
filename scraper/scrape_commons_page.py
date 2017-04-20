#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Get data from file page

import os							# get file path
import sys							# reset file encoding
import webbrowser					# open webpages
import urllib, json, io				# read json
from urllib import urlopen			# open file
from bs4 import BeautifulSoup		# parse html

reload(sys)
sys.setdefaultencoding("utf-8")

# -----------------------------------
# Utilities

folder = os.path.dirname(os.path.realpath(__file__))
t = "\t"
n = "\n"
s = " "

# -----------------------------------
# Script

def get_use(file,project):

	f_out = folder + "/use_on_" + str(project) + ".tsv"
	#print output

	url = "https://commons.wikimedia.org/wiki/File:" + file
	html = urlopen(url) 
	bsObj = BeautifulSoup(html,"html.parser")
	#print bsObj

	with open(f_out, "a") as f:
		
		if project == "commons":
			try: 
				raw_data = bsObj.find("ul",{"class":"mw-imagepage-linkstoimage"}).findAll("li")

				for item in raw_data:
					page = item.get_text().replace(s, "_")
					my_file = file.replace("\n", "")

					output = my_file + t + page
					output_ = output + n
					f.write(output_)
					#print (output)

			except:
				#print("error 1")
				pass

		elif project == "others":
			try: 
				raw_data = bsObj.find("div",{"id":"mw-imagepage-section-globalusage"}).findAll("a",{"class":"external"})
				
				for item in raw_data:
					pag = item.get("href")
					page = "https:" + page
					
					output = file + t + page
					output_ = output + n
					f.write(output_)
					#print (output)
					
			except:
				#print("error 2")
				pass

def get_img_typology(file):
	f_out = folder + "/typology" + ".tsv"

	url = "https://commons.wikimedia.org/wiki/" + file
	html = urlopen(url) 
	bsObj = BeautifulSoup(html,"html.parser")
	#print bsObj

	with open(f_out, "a") as f:
		raw_data = bsObj.find("table",{"id":"mw_metadata"}).find("tr",{"class":"exif-make"}).find("td")

		fil = file.replace(s,"_").replace(n,"")

		# header = file,size,user

		for item in raw_data:
			try:
				tex = item.get_text().replace(s, "_")
				text = tex.replace(n," ")

				output = fil + t + text
				output_ = output + n

				f.write(output_)
				#print(output)
			
			except:
				print(url)
				pass

def get_list(tsv_list):
	file = folder + "/" + tsv_list + ".tsv"
	index = 0

	with open(file, "rb") as in_file:
		#in_file = csv.reader(in_file, delimiter = t)
		filecontent = [line for line in in_file]

		for image in filecontent:
			index += 1

			try:
				#i = ", ".join(image)
				img = str(image)
				#print (img)

				# get_use(img,"commons") # commons other
				get_img_typology(img)
				print(str(index))

			except:
				print (str(index))
				pass


# -----------------------------------
# Launch scripts

#get_use("Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg","others")  #commons others
get_list("data/raw/20170407_a_Media_contributed_by_the_ETH-Bibliothek") # test/test data/raw/20170407_a_Media_contributed_by_the_ETH-Bibliothek


