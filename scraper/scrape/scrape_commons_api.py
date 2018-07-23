#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Scrape data and open web pages

import os						# get file path
import webbrowser				# open webpages
import time						# get unix code
import datetime					# convert in unix timestamp
import urllib, json, io			# read json
from urllib import urlopen		# open file
import sys						# reset file encoding
import datetime					# print time
import csv						# read csv
import re						# replace all occurrences
import pprint					# pretty print
from multiprocessing import Pool
# from multiprocessing import Process

reload(sys)
sys.setdefaultencoding("utf-8")

# -----------------------------------
# Utilities

folder = os.path.dirname(os.path.realpath(__file__))
t = "\t"
n = "\n"
lic = ""
s = " "


def time():
	my_format = "%d %m %Y %I:%M%p" 
	ts = datetime.datetime.utcnow().strftime(my_format)
	print(ts)

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
# main variables

# -----------------------------------
# scripts

def img_info(f_name):
	start = time.time()

	func = "img-timestamp"
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_" + func + "-output.tsv" 
	f_err = folder + "/data/" + f_name + "_" + func + "-errors.tsv" 
	
	with open(f_in, "r") as f1:
		with open(f_out, "w") as f2:
			with open(f_err, "w") as f3:

				for file in f1:

					request = base_api + "&" + api_fileInfo + "&" + proprierties_1 + "&titles=" + file #proprierties_1
					#print(request)

					response = urlopen(request).read()
					data = json.loads(response)
				
					for x in data["query"]["pages"]:
						id_ = str(x)
					
					for y in data["query"]["pages"].values():

						try:
							title = y["title"]
							values = y["imageinfo"]

							for z in values:
								try:
									
									# timestamp = z["timestamp"]
									license = z["extmetadata"]["LicenseShortName"]["value"]
									categories = z["extmetadata"]["Categories"]["value"]
									artist = z["extmetadata"]["Artist"]["value"]
									description = z["extmetadata"]["ImageDescription"]["value"]

									output =  title + t + timestamp + t + categories + t + license + t + re.sub(r"\n", "", artist) + t + re.sub(r"\n", "", description) + n
									print index

								except:
									print("error 2")
									print(request)
									f3.write(title)
									pass

							f2.write(output)

						except:
							print("error 1")
							print(request)
							f3.write(title)
							pass
						
	end = time.time()
	running_time = end - start
	print (running_time)
						
def img_size(f_name):
	time()
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/" + f_name + "-output_imgSize.tsv"
	
	with open(f_in, "r") as f1:
		with open(f_out, "w+") as f2:
			for file in f1:
				# f2.write(line) 
				# print(line)

				request = base_api + "&" + api_fileInfo + "&" + proprierties_3 + "&titles=" + file
				#print(request)

				response = urlopen(request).read()
				data = json.loads(response)
			
				index += 1
				#print(data)
				
				for x in data["query"]["pages"]:
					id_ = str(x)
				
				for y in data["query"]["pages"].values():

					try:
						title = y["title"]
						values = y["imageinfo"]

						for z in values:
							try:

								size = z["size"]
								width = z["width"]
								height = z["height"]
										
								output =  title + t + str(size) + t + str(width) + t + str(height) + n
								print index

							except:
								print(request)
								pass

							f2.write(output)

					except:
						print("error 1 "  + str(index))
						pass

def img_timestamp(f_name,start_id):
	start = time.time()

	func = "img-timestamp"
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_" + func + "-output.tsv" 
	f_err = folder + "/data/" + f_name + "_" + func + "-errors.tsv" 
	
	with open(f_in, "r") as f1:
		with open(f_out, "a+") as f2:
			for file in f1:

				request = base_api + "&" + api_fileInfo + "&" + proprierties_1 + "&titles=" + file
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
									
									output =  str(index) + t + title + t +  extension + t + timestamp + t + license + t + mediatype + n # 
									print (index)

								except:
									print("error 2")
									print(request)
									pass

								f2.write(output)

					except:
						print("error 1")
						print(request)
						pass

				index += 1

	end = time.time()
	running_time = end - start
	print (running_time)

# -----------------------------------
# Launch scripts

img_timestamp("my_data",0)  # data 1_raw/20180620_Media_contributed_by_the_ETH-Bibliothek

#img_info("data") 
#img_size("data") 

# more_img_info("test/test") # eth_files_list test_2
# files_containing_word("in der Serengeti")


