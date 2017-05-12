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

reload(sys)
sys.setdefaultencoding("utf-8")

# -----------------------------------
# Utilities

folder = os.path.dirname(os.path.realpath(__file__))
t = "\t"
n = "\n"
lic = ""
s = " "

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
proprierties_2 = "iiprop=mediatype|extmetadata|timestamp|user|size|mime|metadata&prop=imageinfo&iimetadataversion=latest"

glam_user = "aiuser=ETH-Bibliothek"
api_fileInfo = "prop=imageinfo"


# -----------------------------------
# Main variables

# -----------------------------------
# SCRIPTS

def time():
	my_format = "%d %m %Y %I:%M%p" 
	ts = datetime.datetime.utcnow().strftime(my_format)
	print(ts)

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
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"  # test / data
	f_out = folder + "/test/" + f_name + "-output_.tsv" 
	
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
				#print(data)
				
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
								print("error 2")
								pass

						f2.write(output)

					except:
						#print("error 1")
						pass

def more_img_info(f_name):
	index = 0

	f_in = folder + "/" + f_name + ".tsv"  # test / data
	f_out = folder + "/" + f_name + "_digital.tsv" 
	
	with open(f_in, "r") as f1:
		with open(f_out, "w") as f2:

			for file in f1:
				# f2.write(line) 
				# print(line)

				f = file.replace(s,"_").replace("&","%26").replace("+","%2B")

				request = base_api + "&" + api_fileInfo + "&" + proprierties_2 + "&titles=" + f
				#print(request)

				response = urlopen(request).read()
				data = json.loads(response)
			
				index += 1
				#print(index)
				# print(request)
				# print(data)
				
				for x in data["query"]["pages"]:
					id_ = str(x)
				
				for y in data["query"]["pages"].values():

					try:
						title = y["title"]
						values = y["imageinfo"]
						#print(values)

						for z in values:
							try:
								timestamp = z["timestamp"]
								user = z["user"]
								license = z["extmetadata"]["LicenseShortName"]["value"]
								categories = z["extmetadata"]["Categories"]["value"]
								size = str(z["size"]) # byte
								width = str(z["width"])
								height = str(z["height"])
								source = z["metadata"]

								for so in source:
									try:
										name = so["name"]
										value = so["value"]
										#print(value)

										if name == "exif":
											for va in value:  # all metadata
												a = va["name"] 
												b = va["value"]
												# print(a + "-" + b)

												if a == "Make":
													sou = b
													#print(sou)

									except:
										#print("  " + request)
										pass

								#output =  title + t + timestamp + t + user + t + license + t + categories + t + size + t + width + t + height + t + sou
								output =  str(index) + t + title + t + size + t + width + t + height
								output_ = output + n
								print(index)

							# except IOError:
							# 	print('An error occured trying to read the file.' + n + request)
							# 	pass

							# except ImportError:
							# 	print ("NO module found" + n + request)
							# 	pass
								
							# except EOFError:
							# 	print('Why did you do an EOF on me?' + n + request)
							# 	pass

							# except KeyboardInterrupt:
							# 	print('You cancelled the operation.' + n + request)
							# 	pass

							except:
								#print(request)
								pass

						#print(output)
						f2.write(output_)

					# except IOError:
					# 	print('An error occured trying to read the file.')
					# 	pass

					# except ImportError:
					# 	print "NO module found"
					# 	pass
						
					# except EOFError:
					# 	print('Why did you do an EOF on me?')
					# 	pass

					# except KeyboardInterrupt:
					# 	print('You cancelled the operation.')
					# 	pass

					except:
						output_a = str(index) + t + request
						output_b_ = str(index) + t + title + t + "error" + n
						print(output_a)
						f2.write(output_b_)
						pass

def files_containing_word(word):
	index = 0

	api = "https://en.wikipedia.org/w/api.php?action=query&list=allimages&ailimit=50&aiprop=dimensions%7Cmime&format=json&aifrom="

	request = api + word
	print(request)

	response = urlopen(request).read()
	data = json.loads(response)

	index += 1
	print(index)


# -----------------------------------
# Launch scripts

more_img_info("test/test") # eth_files_list test_2

# get_data(api,my_limit);
# img_info("Media_contributed_by_the_ETH-Bibliothek_2") 
# files_containing_word("in der Serengeti")


