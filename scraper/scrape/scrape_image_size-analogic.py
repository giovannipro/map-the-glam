#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Get data from file page

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
# from multiprocessing import Process

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
# Script

def get_img_size_analogic(f_name,start_id):
	# start = time.time()
	# print(start)

	func = "img_size_analogic"
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_" + func + "-output_2.tsv" 
	f_err = folder + "/data/" + f_name + "_" + func + "-errors_2.tsv" 

	with open(f_in, "r") as f1:
		with open(f_out, "a") as f2:
			with open(f_err, "a") as f3:

				tsv_file = csv.reader(f1, delimiter="\t")

				for file in tsv_file:
					index += 1
					file_id = file[0]
					file_name = file[1]
					# print(file_name)

					if (index >= start_id):

						try:
							url = commons_page + file_name
							html = urlopen(url) 
							bsObj = BeautifulSoup(html,"html.parser")
							print(file_id)

							with open(f_out, "a") as f:
								try:
									raw_data = bsObj.find("div",{"class":"commons-file-information-table"})
									
									output = str(file_id) + t + file_name + t
									f2.write(output)

									f2.write("-" + t)
									# try:
									# 	value_1 = raw_data.findAll("tr")[1].findAll("td")[1].get_text().replace(n,s)
									# 	#.split(s)[2] # h = dimension.split(s)[0]
									# 	# print(value_1)
									# 	f2.write(value_1 + t)
									# except Exception as e:
									# 	output = str(file_id) + t + commons_page+file_name + t + "error 3.1"
									# 	# print(output + str(e))
									# 	f2.write("-" + t)
									# 	f3.write(output + n)
									# 	pass

									f2.write("-" + t)
									# try:
									# 	value_2 = raw_data.findAll("tr")[2].findAll("td")[1].get_text().replace(n,s)
									# 	#.split(s)[2] # h = dimension.split(s)[0]
									# 	# print(value_2)
									# 	f3.write(value_2 + t)
									# except Exception as e:
									# 	output = str(file_id) + t + commons_page+file_name + t + "error 3.2"
									# 	# print(output + str(e))
									# 	f2.write("-" + t)
									# 	f3.write(output + n)
									# 	pass

									try:
										value_3 = raw_data.findAll("tr")[3].findAll("td")[1].get_text().replace(n,s)
										#.split(s)[2] # h = dimension.split(s)[0]
										# print(value_3)
										f2.write(value_3 + t)
									except Exception as e:
										output = str(file_id) + t + commons_page+file_name + t + "error 3.3"
										# print(output + str(e))
										f2.write("-" + t)
										f3.write(output + n)

									try:
										value_4 = raw_data.findAll("tr")[4].findAll("td")[1].get_text().replace(n,s)
										#.split(s)[2] # h = dimension.split(s)[0]
										# print(value_4)
										f2.write(value_4 + t)
									except Exception as e:
										output = str(file_id) + t + commons_page+file_name + t + "error 3.4"
										# print(output + str(e))
										f2.write("-" + t)
										f3.write(output + n)
										pass

									try:
										value_5 = raw_data.findAll("tr")[5].findAll("td")[1].get_text().replace(n,s)
										#.split(s)[2] # h = dimension.split(s)[0]
										# print(value_5)
										f2.write(value_5 + t)
									except Exception as e:
										output = str(file_id) + t + commons_page+file_name + t + "error 3.5"
										# print(output + str(e))
										f2.write("-" + t)
										f3.write(output + n)
										pass

									f2.write("-" + t)
									# try:
									# 	value_6 = raw_data.findAll("tr")[6].findAll("td")[1].get_text().replace(n,s)
									# 	#.split(s)[2] # h = dimension.split(s)[0]
									# 	# print(value_6)
									# 	f2.write(value_6 + t)
									# except Exception as e:
									# 	output = str(file_id) + t + commons_page+file_name + t + "error 3.6"
									# 	# print(output + str(e))
									# 	f2.write("-" + t)
									# 	f3.write(output + n)

									f2.write(n)

								except Exception as e:
									output = str(file_id) + t + commons_page+file_name + t + "error 2"
									print(e)
									f3.write(output + n)
									pass

						except Exception as e:
							output = str(file_id) + t + commons_page+file_name + t + "error 1"
							print(e)
							f3.write(output + n)
							pass
	
	# end = time()
	# running_time = end - start
	# print (running_time)


# -----------------------------------
# Launch scripts

get_img_size_analogic("test",48766);


