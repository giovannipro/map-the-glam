#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Get data from file page

import os							# get file path
import sys							# reset file encoding
import webbrowser					# open webpages
import urllib, json, io				# read json
from urllib import urlopen			# open file
from bs4 import BeautifulSoup		# parse html
import datetime						# print time
import csv							# read csv

reload(sys)
sys.setdefaultencoding("utf-8")

# -----------------------------------
# Utilities

folder = os.path.dirname(os.path.realpath(__file__))
t = "\t"
n = "\n"
s = " "

def time():
	my_format = "%d %m %Y %I:%M%p" 
	ts = datetime.datetime.utcnow().strftime(my_format)
	print(ts)

commons_category_page = "https://commons.wikimedia.org/wiki/Category:"
	
def clean_url(title):
	replace_01 = "?"
	replace_02 = "&"
	replace_03 = "ä"
	replace_04 = "ö"
	replace_06 = "("
	replace_07 = ")"
	replace_08 = ","
	replace_10 = "…"
	replace_11 = " "
	replace_12 = "å"
	replace_13 = "ü"
	replace_14 = ","
	replace_15 = "á"
	replace_16 = '"'
	replace_17 = '?'
	replace_18 = "å"
	replace_19 = "é"
	replace_20 = "ô"
	replace_21 = "è"
	replace_22 = "_"
	replace_23 = " "
	replace_24 = '?'
	replace_25 = '&'

	clean = title \
		.replace(replace_01,"%3f") \
		.replace(replace_02,"%26") \
		.replace(replace_03,"%e4") \
		.replace(replace_04,"%f6") \
		.replace(replace_06,"%28") \
		.replace(replace_07,"%29") \
		.replace(replace_08,"%2c") \
		.replace(replace_10,"%20") \
		.replace(replace_11,"_") \
		.replace(replace_12,"%e5") \
		.replace(replace_13,"%fc") \
		.replace(replace_14,"%2c") \
		.replace(replace_15,"%e1") \
		.replace(replace_16,"%22") \
		.replace(replace_17,"%3f") \
		.replace(replace_18,"ä") \
		.replace(replace_19,"%e9") \
		.replace(replace_20,"%f4") \
		.replace(replace_21,"%e8") \
		.replace(replace_22,"_") \
		.replace(replace_23,"_") \
		.replace(replace_24,"%3f") \
		.replace(replace_25,"%26")

	return clean

# -----------------------------------
# Script

def get_glams_list(f_name):
	func = "glams_list"
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_" + func + "-output.tsv" 
	f_err = folder + "/data/" + f_name + "_" + func + "-errors.tsv" 

	with open(f_in, "r") as f1:
		with open(f_out, "a") as f2:
			with open(f_err, "a") as f3:
				
				def get_categories(url,max_repeat):		
					while max_repeat > 0:
						max_repeat-=1
						try:
							page = commons_category_page + clean_url(url)
							html = urlopen(page) 
							bsObj = BeautifulSoup(html,"html.parser")
							# print(page) # html, bsObj

							categories = bsObj.findAll("div",{"class":"CategoryTreeItem"})

							for cat in categories:
								try:
									the_cat = cat.find("a").string
									count = cat.findAll("span")[-1].string
									output = the_cat + t + count + t + str(max_repeat)
									
							 		print (output)
									f2.write(str(output) + n)

									get_categories(the_cat,max_repeat)

								except Exception as e:
									output = url
									# print(e) #  + " error 2"
									f3.write(str(output) + n)
									pass

						except Exception as e:
							output = url
							# print(e)  #+ " error 1"
							f3.write(str(output) + n)
							pass

				tsv_file = csv.reader(f1, delimiter=t)

				for url in tsv_file:
					url_ = url[1]

					print(str(index) + t + url_ + t +" <<<")
					get_categories(url_,2)



# -----------------------------------
# Launch scripts

get_glams_list("commons_category")  # commons_category test

