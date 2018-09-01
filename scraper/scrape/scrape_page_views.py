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

def scrape_w_pv(proj,f_name,start,end):
	# print(article,start,end)
	# time()

	func = "wiki_pv"
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

									output = str(file_id) + t + file + t + link + t + lang + t + typo + t + str(timestamp) + t + str(views)
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
						link = row[3]
						lang = row[4]
						art = row[5]
						typo = row[6]
						index += 1

						# article = art.replace(" ","+")
						article = urllib.quote_plus(art).replace("+","_")
						timespan = start + "/" + end

						if (proj == "wikipedia"):
							project = lang + ".wikipedia"
						elif (proj == "commons"):
							project = "commons.wikimedia"

						request = root_api + project + "/all-access/user/" + article + "/monthly/" + timespan

						# https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/commons.wikimedia/all-access/user/Commons%3AWikiProject+Aviation%2Frecent+uploads%2F2018+January+20/monthly/20150701/20180730
						# https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/commons.wikimedia/all-access/user/Commons%3AWikiProject_Aviation%2Frecent_uploads%2F2017_December_19/monthly/2015070100/2018073100

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

scrape_w_pv("wikipedia","test_w","20160501","20180730") 
# scrape_w_pv("commons","test_c","20150701","20180730")


