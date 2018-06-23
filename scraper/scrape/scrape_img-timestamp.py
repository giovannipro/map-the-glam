#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Scrape data and open web pages

import os						# get file path
import webbrowser				# open webpages
import time		     			# get unix code
import datetime					# convert in unix timestamp
import urllib, json, io			# read json
from urllib import urlopen		# open file
import sys						# reset file encoding
import datetime					# print time
import csv						# read csv
import re						# replace all occurrences
import pprint					# pretty print

# from multiprocessing import Process
from multiprocessing import Pool

reload(sys)
sys.setdefaultencoding("utf-8")

# -----------------------------------
# Utilities

folder = os.path.dirname(os.path.realpath(__file__))
t = "\t"
n = "\n"
lic = ""
s = " "

def clean_url(title):
	replace_01 = "?"
	replace_02 = "&"
	replace_03 = "ä"
	replace_04 = "ö"
	replace_05 = "u"
	replace_06 = "("
	replace_07 = ")"
	replace_08 = ","
	replace_09 = "-"
	replace_10 = "…"
	replace_11 = " "

	clean = title.replace(replace_01,"%3f") \
		.replace(replace_02,"%26") \
		.replace(replace_03,"%e5") \
		.replace(replace_04,"%f6") \
		.replace(replace_05,"%fc") \
		.replace(replace_06,"%28") \
		.replace(replace_07,"%29") \
		.replace(replace_08,"%2c") \
		.replace(replace_09,"%2d") \
		.replace(replace_10,"%20")
	
	return clean

# -----------------------------------
# API

base_api = "https://commons.wikimedia.org/w/api.php?action=query&format=json"

commons_api = "https://commons.wikimedia.org/w/api.php?action=query&format=json&list=allimages&aisort=timestamp"
proprierties_1 = "iiprop=size|mediatype|extmetadata|timestamp|url|mediatype" #&prop=imageinfo|commonmetadata|metadata|"
proprierties_2 = "iiprop=mediatype|extmetadata|timestamp|user|size|mime|metadata&prop=imageinfo&iimetadataversion=latest"
proprierties_3 = "iiprop=size"

glam_user = "aiuser=ETH-Bibliothek"
api_fileInfo = "prop=imageinfo"


# -----------------------------------
# scripts

def img_timestamp(f_name,start_id):
	start = time.time()

	func = "img-timestamp"
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_" + func + "-output.tsv" 
	f_err = folder + "/data/" + f_name + "_" + func + "-errors.tsv" 
	
	with open(f_in, "r") as f1:
		with open(f_out, "a+") as f2:
			with open(f_err, "a+") as f3:

				csv_file = csv.reader(f1, delimiter="\t")

				for file in csv_file:
					title = clean_url(file[1]) #file[1]
					# print title

					request = base_api + "&" + api_fileInfo + "&" + proprierties_1 + "&titles=" + title
					#print(request)

					if (index >= start_id):
						try:
							response = urlopen(request).read()
							data = json.loads(response)
							output = ""
						
							for x in data["query"]["pages"]:
								id_ = str(x)
							
							for y in data["query"]["pages"].values():

								title = y["title"]
								extension = ''.join(y["title"].split(".")[-1:])
								values = y["imageinfo"]

								for z in values:
									try:
									
										timestamp = z["timestamp"]
										license = z["extmetadata"]["LicenseShortName"]["value"]
										mediatype = z["mediatype"]									
										
										output =  str(index) + t + title + t +  extension + t + timestamp + t + license + t + mediatype + n 
										print (index)
										f2.write(output)

									except:
										print("error 2")
										print(request)

										error = str(index) + t + title + n
										f3.write(error)
										pass

						except:
							print("error 1")
							print(request)

							error = str(index) + t + title + n
							f3.write(error)
							pass

					index += 1

	end = time.time()
	running_time = end - start
	print (running_time)

# -----------------------------------
# Launch scripts

img_timestamp("my_data-errors",0)  # data 1_raw/20180620_Media_contributed_by_the_ETH-Bibliothek


