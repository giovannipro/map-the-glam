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
# Main variables

api_old = "http://stats.grok.se/json/en/" # 2008 — 2015
api = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/" # from 2016 

root_api = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"

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

def scrape_pv_after_2016(f_name,start,end):
	# print(article,start,end)

	time()

	f_in = folder + "/" + f_name + ".tsv"
	f_out = folder + "/" + f_name + "-pv.tsv" 
	
	with open(f_in, "r") as f1:
		with open(f_out, "w") as f2:

			tsvin = csv.reader(f1, delimiter = t)
			index = 0

			# lang, article,start,end

			for row in tsvin:

				try:

					file = row[0]
					article = row[1]
					language = row[2]
					#print (article + lang)

					index += 1

					l = language.split("-")[3]
					lang = l.split("_")[0]
					article = article.replace(s,"_").replace(":","%3A").replace("/","%2")
					print (lang)

					timespan = start + "/" + end
					request = root_api + lang + ".wikipedia/all-access/user/" + article + "/daily/" + timespan
					print request

					response = urlopen(request).read()
					data = json.loads(response)
					
					pv = 0
					#print(data)

					for key, value in data.items():
						d = value
						#print(d)

						for x in d:
							views = x["views"]
							timestamp = x["timestamp"]
							output = str(index) + t + article + t + lang + t + timestamp + t + str(views)
							output_ = output + n

							f2.write(output_)
							print (index)
				except:
					output = str(index) + t + request
					output_ = output + n
					print(output)
					f2.write(output_)
					pass

	time()

def scrape_pv_before_2016(article,start,end):
	print(article,start,end)

	for t in range (start,(end + 1)):

		for x in range (1, 13):
			timespan = str(start) + str(add_zero(x))

			request = api_old + timespan + "/" + article
			#print request
			
			response = urlopen(request).read()
			data = json.loads(response)

			for key, value in data["daily_views"].items():
				date = str(key)
				views = str(value)
				output = date + "\t" + views

				print(output)

		start += 1


# -----------------------------------
# Launch script

scrape_pv_after_2016("test/articles","20160101","20170330")

#scrape_pv_after_2016("en","Wikipedia:Graphics Lab/FPhotography workshop","20161231","20170330")
#scrape_pv_before_2016("Day_of_Reconciliation",2008,2015)

'''
https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Wikipedia%3AGraphics_Lab%2FPhotography_workshop/daily/2017042400/2017051400

https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Wikipedia%3Graphics_Lab%2FPhotography_workshop/daily/2016070100/2016033100

'''







