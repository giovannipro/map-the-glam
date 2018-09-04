#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Scrape page views

import os					# get file path
import webbrowser			# open webpages
import time					# get unix code
import datetime				# convert in unix timestamp
import urllib, json, io		# read json
from urllib import urlopen	# open file
import sys					# reset file encoding
import csv					# read csv
import linecache
from operator import itemgetter

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

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

# -----------------------------------
# Main variables

api_old = "http://stats.grok.se/json/en/" # 2008 — 2015
w_api = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/" # from 2016 
root_api = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"

# wmf_api = "https://tools.wmflabs.org/pageviews/?project="
#https://tools.wmflabs.org/pageviews/?project=commons.wikimedia.org&platform=all-access&agent=all-agents&start=2015-07&end=2018-07&pages=Category:Media_contributed_by_the_ETH-Bibliothek

# https://tools.wmflabs.org/pageviews/?project=en.wikipedia.org&platform=all-access&agent=user&range=latest-20&pages=Cat|Dog
# http://stats.grok.se/json/en/200801/hiv
# https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Day_of_Reconciliation/monthly/20120101/20161231

# -----------------------------------
# Script

def add_zero(x):
	if x < 10:
		return "0" + str(x)
	else:
		return x

def scrape_pv(proj,f_name,start,end):
	# print(article,start,end)
	# time()

	func = "pv_data"
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_" + func + "-output.tsv" 
	f_err = folder + "/data/" + f_name + "_" + func + "-errors.tsv" 
	print(func)

	with open(f_in, "r") as f1:
		with open(f_out, "a") as f2:
			with open(f_err, "a") as f3:

				tsv_file = csv.reader(f1, delimiter=t)

				def get_data(request):
					# print (file_id + t + art)
					# print(request)

					response = urlopen(request).read()
					data = json.loads(response)
					# print(data)
					
					for k,v in data.items():
						try:
							for x in v:
								try:
									# print x
									views = x["views"]
									timestamp = x["timestamp"]

									year = timestamp[0:4]
									month = timestamp[4:6]
									day = timestamp[6:8]
									parsed_date = year + "-" + month + "-" + day

									output = str(file_id) + t + file + t + link + t + lang + t + typo + t + parsed_date + t + str(views)
									print(file_id)
									f2.write(output + n)

								except:
									PrintException()
									output = str(index) + t + request + t + "error_2"
									# print(output)
									f3.write(output + n)
									pass
						except:
							PrintException()
							output = str(index) + t + request + t + "error_1"
							# print(output)
							f3.write(output + n)
							pass

				new_art = ""
				count_img = 1;
				for row in sorted(tsv_file, key=itemgetter(5)):
					try:
						file_id = row[0]
						file = row[1]
						page = row[2] # w 2 - c 3
						link = row[2] # w 2 - c 3
						lang = row[3] # w 3 - c "-"
						art = row[3] # w 3 - c 3
						typo = row[4]  # w 4 - c 2
						index += 1

						# 0	File:Aettenschwil 1953.jpg	Aettenschwil	de	article	9340	122	1.30620985011

						# article = art.replace(" ","+")
						article = urllib.quote_plus(art).replace("+","_")
						timespan = start + "/" + end

						if (proj == "wikipedia"):
							project = lang + ".wikipedia"
						elif (proj == "commons"):
							project = "commons.wikimedia"

						request = root_api + project + "/all-access/user/" + article + "/monthly/" + timespan

						if (art != new_art):
							# print(article + t + str(count_img) + t + "<<<<")
							# print (file_id + t + art)
							count_img = 1
							get_data(request)
						else:
							count_img += 1
							# print(article + t + str(count_img))
							# continue
							
						new_art = art
						
					except:
						PrintException()
						output = str(index) + t + request + t + "error_0"
						# print(output)
						f2.write(output + n)
						pass

	# time()

# def scrape_pv_before_2016(article,start,end):
# 	print(article,start,end)

# 	for t in range (start,(end + 1)):

# 		for x in range (1, 13):
# 			timespan = str(start) + str(add_zero(x))

# 			request = api_old + timespan + "/" + article
# 			#print request
			
# 			response = urlopen(request).read()
# 			data = json.loads(response)

# 			for key, value in data["daily_views"].items():
# 				date = str(key)
# 				views = str(value)
# 				output = date + "\t" + views

# 				print(output)

# 		start += 1


# -----------------------------------
# Launch script

scrape_pv("wikipedia","1_raw/w_pages_using_files_wiki_revisions-output","20160401","20180730") 
# scrape_pv("commons","1_raw/c_revisions-output","20160401","20180730")


