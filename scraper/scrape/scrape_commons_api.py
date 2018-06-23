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
from multiprocessing import Pool

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
# API

base_api = "https://commons.wikimedia.org/w/api.php?action=query&format=json"

commons_api = "https://commons.wikimedia.org/w/api.php?action=query&format=json&list=allimages&aisort=timestamp"
proprierties_1 = "iiprop=size|mediatype|extmetadata|timestamp|url|mediatype" #&prop=imageinfo|commonmetadata|metadata|"
proprierties_2 = "iiprop=mediatype|extmetadata|timestamp|user|size|mime|metadata&prop=imageinfo&iimetadataversion=latest"
proprierties_3 = "iiprop=size"

glam_user = "aiuser=ETH-Bibliothek"
api_fileInfo = "prop=imageinfo"


# -----------------------------------
# main variables

# -----------------------------------
# scripts

def img_info(f_name):
	start = time.time()

	func = "img-timestamp"
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_" + func + "-output.tsv" 
	f_err = folder + "/data/" + f_name + "_" + func + "-errors.tsv" 
	
	with open(f_in, "r") as f1:
		with open(f_out, "w") as f2:
			with open(f_err, "w") as f3:

				for file in f1:

					request = base_api + "&" + api_fileInfo + "&" + proprierties_1 + "&titles=" + file #proprierties_1
					#print(request)

					response = urlopen(request).read()
					data = json.loads(response)
				
					for x in data["query"]["pages"]:
						id_ = str(x)
					
					for y in data["query"]["pages"].values():

						try:
							title = y["title"]
							values = y["imageinfo"]

							for z in values:
								try:
									
									# timestamp = z["timestamp"]
									license = z["extmetadata"]["LicenseShortName"]["value"]
									categories = z["extmetadata"]["Categories"]["value"]
									artist = z["extmetadata"]["Artist"]["value"]
									description = z["extmetadata"]["ImageDescription"]["value"]

									output =  title + t + timestamp + t + categories + t + license + t + re.sub(r"\n", "", artist) + t + re.sub(r"\n", "", description) + n
									print index

								except:
									print("error 2")
									print(request)
									f3.write(title)
									pass

							f2.write(output)

						except:
							print("error 1")
							print(request)
							f3.write(title)
							pass
						
	end = time.time()
	running_time = end - start
	print (running_time)
						
def img_size(f_name):
	time()
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/" + f_name + "-output_imgSize.tsv"
	
	with open(f_in, "r") as f1:
		with open(f_out, "w+") as f2:
			for file in f1:
				# f2.write(line) 
				# print(line)

				request = base_api + "&" + api_fileInfo + "&" + proprierties_3 + "&titles=" + file
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

								size = z["size"]
								width = z["width"]
								height = z["height"]
										
								output =  title + t + str(size) + t + str(width) + t + str(height) + n
								print index

							except:
								print(request)
								pass

							f2.write(output)

					except:
						print("error 1 "  + str(index))
						pass

def img_timestamp(f_name,start_id):
	start = time.time()

	func = "img-timestamp"
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_" + func + "-output.tsv" 
	f_err = folder + "/data/" + f_name + "_" + func + "-errors.tsv" 
	
	with open(f_in, "r") as f1:
		with open(f_out, "a+") as f2:
			for file in f1:

				request = base_api + "&" + api_fileInfo + "&" + proprierties_1 + "&titles=" + file
				#print(request)

				if (index >= start_id):
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
									
									output =  str(index) + t + title + t +  extension + t + timestamp + t + license + t + mediatype + n # 
									print (index)

								except:
									print("error 2")
									print(request)
									pass

								f2.write(output)

					except:
						print("error 1")
						print(request)
						pass

				index += 1

	end = time.time()
	running_time = end - start
	print (running_time)
	

"""						
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



def http_get(url):
  result = {"url": url, "data": urllib.urlopen(url).read()[:100]}
  print url + " took "
  return result
  
urls = ['http://www.google.com/', 'https://foursquare.com/', 'http://www.yahoo.com/', 'http://www.bing.com/', "https://www.yelp.com/"]

pool = Pool(processes=5)

results = pool.map(http_get, urls)

for result in results:
  print result

"""  


# -----------------------------------
# Launch scripts

img_timestamp("my_data",0)  # data 1_raw/20180620_Media_contributed_by_the_ETH-Bibliothek

#img_info("data") 
#img_size("data") 

# more_img_info("test/test") # eth_files_list test_2
# files_containing_word("in der Serengeti")


