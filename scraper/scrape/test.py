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

# from multiprocessing import Process
from multiprocessing import Process

reload(sys)
sys.setdefaultencoding("utf-8")


# -----------------------------------
# Utilities

folder = os.path.dirname(os.path.realpath(__file__))
t = "\t"
n = "\n"
lic = ""
s = " "

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

base = "/Users/giovanni/documents/PhD/map-the-glam/scraper/scrape/data/"
f_in = base + "my_data_err.tsv"
f_out = f_in + "_output.tsv" 
f_err_small = f_in + "_err-big.tsv"	
f_err_big = f_in + "_err-big.tsv"	

def test(title):

	start = time.time()
	index = 0

	with open(f_out, "w") as f2:
		with open(f_err_small, "w") as f3, open(f_err_big, "w") as f4:

			for title in titles:
				request = base_api + "&" + api_fileInfo + "&" + proprierties_1 + "&titles=" + title

				# if (index >= start_id):
				if (1 == 1):
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
						f4.write(error)
						pass

					index += 1

	end = time.time()
	running_time = end - start
	print (running_time)
 
if __name__ == '__main__':

	titles = []

	with open(f_in, "r") as f1:
		file = csv.reader(f1, delimiter="\t")

		for x in file:
			tit = x[1]
			clean = x[1].replace(" ","_").replace("ö","%d6")
			titles.append(clean)

		#titles = ["File:BassersdorffSchatz-19801028iv.jpg", "File:BassersdorffSchatz-19810519i.jpg", "File:BassersdorffSchatz-19810519i.tif"]
	 	# print titles

	p = Process(target=test, args=("title",))
	p.start()
	p.join


"""

def test(x):
 
    for x in titles:
    	request = base_api + "&" + api_fileInfo + "&" + proprierties_1 + "&titles=" + x
        print(request)
 
if __name__ == '__main__':
    titles = ["File:BassersdorffSchatz-19801028iv.jpg", "File:BassersdorffSchatz-19810519i.jpg", "File:BassersdorffSchatz-19810519i.tif"]
 
    p = Process(target=test, args=('x',))
    p.start()
    p.join
    print "Done"

"""



