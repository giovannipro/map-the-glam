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

def clean_url_a(title):
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
	# replace_09 = "-"

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
		.replace(replace_17,"%3f")
		# .replace(replace_05,"%fc") 
		# .replace(replace_09,"%2d") \
	
	return clean

def clean_url_b(title):
	replace_01 = "å"
	replace_02 = "é"
	replace_03 = "ô"
	replace_04 = "è"
	replace_05 = "_"
	replace_06 = " "
	replace_07 = '?'
	replace_08 = '&'

	clean = title \
		.replace(replace_01,"ä") \
		.replace(replace_02,"%e9") \
		.replace(replace_03,"%f4") \
		.replace(replace_04,"%e8") \
		.replace(replace_05,"_") \
		.replace(replace_06,"_") \
		.replace(replace_07,"%3f") \
		.replace(replace_07,"%26")

	return clean

# -----------------------------------
# API

base_api = "https://commons.wikimedia.org/w/api.php?action=query&format=json"

commons_api = "https://commons.wikimedia.org/w/api.php?action=query&format=json&list=allimages&aisort=timestamp"
proprierties_1a = "iiprop=size|mediatype|extmetadata|timestamp|url|mediatype" #&prop=imageinfo|commonmetadata|metadata|"
proprierties_1b = "iiprop=size|mediatype|extmetadata|timestamp|url|mediatype" #&prop=imageinfo|commonmetadata|metadata|"

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

					request = base_api + "&" + api_fileInfo + "&" + proprierties_1a + "&titles=" + title
					#print(request)

					if (index >= start_id):
						try:
							response = urlopen(request).read()
							data = json.loads(response)
							output = ""
						
							for x in data["query"]["pages"]:
								id_ = str(x)
							
							for y in data["query"]["pages"].values():

								try:
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
											print("error 3")
											print(request)

											error = str(index) + t + title + n
											f3.write(error)
											pass
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

def img_metadata(f_name,start_id):
	start = time.time()
	print(start)

	func = "img-metadata"
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_" + func + "-output.tsv" 
	f_err = folder + "/data/" + f_name + "_" + func + "-errors.tsv" 
	
	with open(f_in, "r") as f1:
		with open(f_out, "a+") as f2:
			with open(f_err, "a+") as f3:

				csv_file = csv.reader(f1, delimiter="\t")

				for file in csv_file:
					# title = file[1]
					title = clean_url_a(clean_url_b(file[1]))
					my_id = file[0]
					# title = clean_url(file[1])
					# print title

					request = base_api + "&" + api_fileInfo + "&" + proprierties_1b + "&titles=" + title
					# print(request)

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
								# print(extension)

								for z in values:
									try:
										# timestamp = z["timestamp"]
										# license = z["extmetadata"]["LicenseShortName"]["value"]
										#mediatype = z["mediatype"]			
										categories = z["extmetadata"]["Categories"]["value"]
										
										print (my_id)
										f2.write(str(my_id) + t + file[1] + t + categories + t)

										try:
											size = z["size"]
											width = z["width"]
											height = z["height"]
											output_a =  str(size) + t + str(width) + t + str(height) + t
											f2.write(output_a)
										except Exception as e: 
											print(e)
											output_b = "-" + t + "-" + t + "-" + t
											f2.write(output_b)
											pass

										try:
											imageDescription = z["extmetadata"]["ImageDescription"]["value"]
											imageDescription_clean = imageDescription.replace('<span class=\"description\">\n',"").replace("</span>","").replace('<span class="description">',"").replace("<span class=\"description\">\n","").replace("\n"," ")
											f2.write(imageDescription_clean + t)
										except:
											f2.write("-" + t)
											pass

										try:
											dateTimeOriginal = z["extmetadata"]["DateTimeOriginal"]["value"]
											dateTimeOriginal_clean = dateTimeOriginal.replace("\n"," ")
											f2.write(dateTimeOriginal_clean + t)	
										except:
											f2.write("-" + t)
											pass

										try:
											artist = z["extmetadata"]["Artist"]["value"]
											artist_clean = artist.replace('<span class=\"fn value\">\n',"").replace("</span>","").replace("\n"," ")		
											f2.write(artist_clean + t)	
										except:
											f2.write("-")
											pass

										f2.write(n)
											
									except:
										print("error 2")
										print(request)

										error = str(my_id) + t + file[1] + n
										f3.write(error)
										pass

						except:
							print("error 1")
							print(request)

							error = str(my_id) + t + file[1] + n
							f3.write(error)
							pass

					index += 1

	end = time.time()
	running_time = end - start
	print (running_time) # in milliseconds

def test(n):
	for a in range(n):
		print a

# -----------------------------------
# Launch scripts

# img_timestamp("test_data",0)

img_metadata("test_data_img-metadata-errors_img-metadata-errors",0) # data 1_raw/20180620_Media_contributed_by_the_ETH-Bibliothek


