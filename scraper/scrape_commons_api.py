#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Scrape data and open web pages

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

def unix_time(mytime):
	u_time = time.mktime(datetime.datetime.strptime(mytime, "%d_%m_%Y_%H:%M").timetuple())
	return str(int(u_time))

def add_zero(x):
	if (int(x) < 10):
		x = "0" + str(x)
		return x
	else:
		return str(x)

# -----------------------------------
# API

base_api = "https://commons.wikimedia.org/w/api.php?action=query&format=json"

commons_api = "https://commons.wikimedia.org/w/api.php?action=query&format=json&list=allimages&aisort=timestamp"
proprierties = "iiprop=mediatype|extmetadata|timestamp&prop=imageinfo"  # |commonmetadata|metadata|
glam_user = "aiuser=ETH-Bibliothek"

api_fileInfo = "prop=imageinfo"

# -----------------------------------
# SCRIPTS

def get_data(api,my_limit):

	file = folder + "/" + "data_2" + ".tsv"

	with open(file, "a") as f:

		response = urlopen(api).read()
		data = json.loads(response)
		index = 0
		#json.dump(data, f)

		for x in data["query"]["allimages"]:

			try:
				tit = x["name"]
				tim = x["timestamp"]
				cat = x["extmetadata"]["Categories"]["value"]
				lic = x["extmetadata"]["LicenseShortName"]["value"]
				des = x["extmetadata"]["ImageDescription"]["value"]

				if (tit != ""):
					f.write(tit + t)
				else:
					f.write("-" + t)

				if (tit != ""):
					f.write(tim + t)
				else:
					f.write("-" + t)

				if (cat != ""):
					f.write(cat + t)
				else:
					f.write("-" + t)
					#print cat 

				if (lic != ""):
					f.write(lic)
				else:
					f.write("-")

				f.write(n)

				index += 1

				if (index == (my_limit-0) ):
					print "LIMIT REACHED: " + tit
					# print index + "+" + my_limit
				# else:
				# 	# print index + "-" + my_limit
				# 	print "-" + str(index)

			except IOError:
				print('An error occured trying to read the file.')
				continue

			except ImportError:
				print "NO module found"
				continue
				
			except EOFError:
				print('Why did you do an EOF on me?')
				continue

			except KeyboardInterrupt:
				print('You cancelled the operation.')
				continue

			except:
				#print('An error occured.')
				index += 1
				
				if (index == (my_limit-0) ):
					print "LIMIT REACHED: " + tit
						
				print (tit + t + tim + t + cat + t + lic)

				continue

def every_day(year,period,my_limit):
	limit = "ailimit=" + str(my_limit)

	if (period == 1):
		start = 1
		end = (6 + 1)
	elif (period == 2):
		start = 7
		end = (12 + 1)	
	else:
		start = 1
		end = (12 + 1)		

	for m in range(start,end):
		try:
			month = add_zero(m)

			for d in range(1,(31 + 1)):
				day = add_zero(d)

				timespan = "aistart=" + unix_time(day + "_" + month + "_2016_00:00") + "&" + "aiend=" + unix_time(day + "_" + month + "_2016_23:59")
				# print timespan

				api = commons_api + "&" + proprierties + "&" + limit + "&" + glam_user + "&" + timespan 

				get_data(api,my_limit)
		except:
			continue

def every_hour(day,mon,my_limit):
	limit = "ailimit=" + str(my_limit)
	day = add_zero(day)
	month = add_zero(mon) 

	for h in range(0,(23 + 1)):
		hour = add_zero(h)
		#print month

		date = day + "_" + month + "_2016_" + hour
		timespan = "aistart=" + unix_time(date + ":00") + "&" + "aiend=" + unix_time(date + ":59")

		api = commons_api + "&" + proprierties + "&" + limit + "&" + glam_user + "&" + timespan 
		#print date

		get_data(api,my_limit)

def img_info(f_name):
	f_in = folder + "/data/" + f_name + ".tsv"  # test / data
	f_out = folder + "/test/" + f_name + "-output_.tsv" 
	index = 0
	
	with open(f_in, "r") as f1:
		with open(f_out, "w") as f2:
			for file in f1:
				# f2.write(line) 
				# print(line)

				request = base_api + "&" + api_fileInfo + "&" + proprierties + "&titles=" + file
				#print(request)

				response = urlopen(request).read()
				data = json.loads(response)
			
				index += 1
				print(index)
				#print(data)

				# head = "title" + t + "timestamp" + t + "categories" + t + "license" + n
				
				for x in data["query"]["pages"]:
					id_ = str(x)
				
				for y in data["query"]["pages"].values():

					try:
						title = y["title"]
						values = y["imageinfo"]

						for z in values:
							try:
								timestamp = z["timestamp"]
								license = z["extmetadata"]["LicenseShortName"]["value"]
								categories = z["extmetadata"]["Categories"]["value"]
								user = z["extmetadata"]["Artist"]["value"]

								output =  title + t + timestamp + t + categories + t + license + n
							except:
									pass

						f2.write(output)

					except:
						pass

# -----------------------------------
# Launch scripts

#get_data(api,my_limit);
img_info("Media_contributed_by_the_Swiss_Federal_Archives") 
