#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Get data abaout file usage

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
from bs4 import BeautifulSoup		# parse html
from multiprocessing import Pool

reload(sys)
sys.setdefaultencoding("utf-8")

# -----------------------------------
# Utilities

folder = os.path.dirname(os.path.realpath(__file__))
t = "\t"
n = "\n"
s = " "

commons_page = "https://commons.wikimedia.org/wiki/"

def time():
	my_format = "%d %m %Y %I:%M%p" 
	ts = datetime.datetime.utcnow().strftime(my_format)
	print(ts)

# -----------------------------------
# Script

def get_file_usage(f_name,start_id):

	func = "file_usage"
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_" + func + "-output.tsv" 
	f_err = folder + "/data/" + f_name + "_" + func + "-errors.tsv" 

	with open(f_in, "r") as f1:
		with open(f_out, "a") as f2:
			with open(f_err, "a") as f3:

				tsv_file = csv.reader(f1, delimiter=t)

				for file in tsv_file:
					index += 1
					file_id = file[0]
					file_name = file[1]
					# print(file_name)

					count_c = 0
					count_e = 0

					if (index >= start_id):
						try:
							url = commons_page + file_name
							html = urlopen(url) 
							bsObj = BeautifulSoup(html,"html.parser")

							# commons usage
							try:
								commons_usage = bsObj.find("ul",{"class":"mw-imagepage-linkstoimage"}).findAll("a")

								for a in commons_usage:
									count_c+=1
									link = a["href"] 
									c_page = a.contents[0] 
									output = str(file_id) + t + file_name + t + "commons" + t + link + t + c_page
									f2.write(output + n)
							except Exception as e:
								# output = str(file_id) + t + commons_page+file_name + t + "error 2"
								# print(output)
								# print(e)
								# f3.write(output + n)
								pass

							# external usage
							try:
								external_usage = bsObj.find("div",{"id":"mw-imagepage-section-globalusage"}).findAll("a",{"class":"external"})
								
								for a in external_usage:
									count_e+=1
									link = a["href"] 
									e_page = a.contents[0] 
									output = str(file_id) + t + file_name + t + "external" + t + link + t + e_page
									f2.write(output + n)
							except Exception as e:
								# output = str(file_id) + t + commons_page+file_name + t + "error 3"
								# print(output)
								# print(e)
								# f3.write(output + n)
								pass

							print(str(file_id) + t + str(count_c) + t + str(count_e))

						except Exception as e:
							output = str(file_id) + t + commons_page+file_name + t + "error 1"
							print(output)
							print(e)
							f3.write(output + n)
							pass


# -----------------------------------
# Launch scripts

get_file_usage("test_usage",0); # test_data test


