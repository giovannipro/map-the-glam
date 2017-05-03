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
# Main variables

api_old = "http://stats.grok.se/json/en/" # 2008 — 2015
api = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/" # from 2016 

# http://stats.grok.se/json/en/200801/hiv
# https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/Day_of_Reconciliation/monthly/20120101/20161231

# -----------------------------------
# Script

def add_zero(x):
	if x < 10:
		return "0" + str(x)
	else:
		return x

def scrape_pv_after_2016(article,start,end):
	print(article,start,end)

	timespan = start + "/" + end
	request = api + article + "/daily/" + timespan
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
			output = timestamp + t + str(views)

			print (output)

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

scrape_pv_after_2016("Day_of_Reconciliation","20160701","20161231")
#scrape_pv_before_2016("Day_of_Reconciliation",2008,2015)

