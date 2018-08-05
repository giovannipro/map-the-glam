#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Get files in category

import os							# get file path
import sys							# reset file encoding
import webbrowser					# open webpages
import urllib, json, io				# read json
from urllib import urlopen			# open file
import time		     			# get unix code
import csv							# read csv

reload(sys)
sys.setdefaultencoding("utf-8")

# -----------------------------------
# Utilities

folder = os.path.dirname(os.path.realpath(__file__))
t = "\t"
n = "\n"
s = " "

def loop(x):
		
	index = 0

	while index < x:
		index += 1
		print(index)

def inloop(x):
	print (x)

	index = x

	if index < x:
		index -= 1
		inloop(index)

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

# test = clean_url("?????")
# print test


# -----------------------------------
# Main variables

commons_api = "https://commons.wikimedia.org/w/api.php?action=query&format=json&list=categorymembers&cmtitle=Category:"
limit = 500

# -----------------------------------
# Script


def get_files(category,cont):
	counter = 0
	
	f_out = folder + "/data/" + str(category) + ".tsv"

	if cont == 0:
		request = commons_api + category + "&cmlimit=" + str(limit)
	else:
		request = commons_api + category + "&cmlimit=" + str(limit) + "&cmcontinue=" + str(cont) # &rvcontinue=

	response = urlopen(request).read()
	data = json.loads(response)

	with open(f_out, "w") as f: # a: add, w+: override
		
		for x in data["query"]["categorymembers"]:

			try: 
				title = x["title"];
				output = title + n

				counter+=1

				f.write(output)
				print(counter)

			except:
				pass

		# index = 0	
			try:
				new_new_cont = data["continue"]["cmcontinue"]

				if (new_new_cont != 0 and new_new_cont != cont): 
					get_files(category,new_new_cont)
					# index += 1
					# print(index)
				else:
					print("stop")
			except:
				pass


def check_files(f_name):
	start = time.time()

	func = "check-files"

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "-" + func + "_out.tsv"
	f_err = folder + "/data/" + f_name + "-" + func + "_err.tsv"

	with open(f_in, "r") as f1:
		with open(f_out, "w") as f2:
			with open(f_err, "w") as f3:

				tsvin = csv.reader(f1, delimiter = t)

				def remove_duplicates(values):
				    output = []
				    seen = set()
				    for value in values:
				        if value not in seen:
				            output.append(value)
				            seen.add(value)			        	
				    return output

				def if_exist(titles):
					output = []
					ind = 0

					for title in titles:

						try:
							request = "https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=timestamp&titles=" + title
							response = urlopen(request).read()
							data = json.loads(response)

							for x in data["query"]["pages"]:
								id_ = int(x)

								if (id_ > 0):
									# output = f2.write(title + n)
									output.append(title)
									print str(ind) # + t + title
								else:
									f3.write(title + n)
									print str(ind) + t + title # + "<<<< error 1"

								ind += 1

						except:
							f3.write(title + n)
							print str(ind) + t + title # + " <<<< error 2"
							pass

					return output

				check = "File:"
				replace_01 = "?"
				replace_02 = "&"
				replace_03 = "ä"
				replace_04 = "ö"
				replace_05 = "u"

				list_ = []

				for file in tsvin:
					title = file[1].replace(replace_01,"%3f").replace(replace_02,"%26").replace(replace_03,"%e5").replace(replace_04,"%f6").replace(replace_05,"%fc")
	
					if (check in title):
						list_.append(title)
					else:
						f3.write(title)
				
				result_1 = remove_duplicates(list_)

				result_2 = if_exist(result_1)

				index = 0
				for final in result_2:
					output = str(index) + t + final + n
					f2.write(output)
					index +=1

	end = time.time()
	running_time = end - start
	print (running_time)				

"""
def test():

	check = "File:"
	replace_01 = "?"
	replace_02 = "&"

	list_ = ["erjnfdc", "File:33","daix?", "fe?cdiwsb?"]

	for x in list_:
		clean = x.replace(replace_01,"xxx")
		print(clean)
"""

# -----------------------------------
# Launch scripts


# check_files("Media_contributed_by_the_ETH-Bibliothek")

# test()

# get_files("Media_contributed_by_the_ETH-Bibliothek",0) # Media_contributed_by_the_Swiss_National_Library Media_contributed_by_the_Swiss_Federal_Archives Media_contributed_by_the_Swiss_Federal_Archives Media_contributed_by_the_ETH-Bibliothek
get_files("GWToolset Batch Upload",0)

