#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Get data from file page

import os							# get file path
import sys							# reset file encoding
import webbrowser					# open webpages
import urllib, json, io				# read json
from urllib import urlopen			# open file
from bs4 import BeautifulSoup		# parse html
import datetime						# print time

reload(sys)
sys.setdefaultencoding("utf-8")

# -----------------------------------
# Utilities

folder = os.path.dirname(os.path.realpath(__file__))
t = "\t"
n = "\n"
s = " "

def time():
	my_format = "%d %m %Y %I:%M%p" 
	ts = datetime.datetime.utcnow().strftime(my_format)
	print(ts)
	
# -----------------------------------
# Script

def get_usage(f_name):

	time()

	f_in = folder + "/" + f_name + ".tsv"  # test / data
	f_out = folder + "/" + f_name + "-usage.tsv" 
	
	with open(f_in, "r") as f1:
		with open(f_out, "w") as f:
			filecontent = [line for line in f1]
			index = 0

			for image in filecontent:
				index += 1

				try:
					url = "https://commons.wikimedia.org/wiki/" + image
					html = urlopen(url) 
					bsObj = BeautifulSoup(html,"html.parser")
					#print bsObj

					commons_data = bsObj.find("ul",{"class":"mw-imagepage-linkstoimage"}).findAll("li")

					if commons_data != "":

						for item in commons_data:
							try:
								page = item.get_text().replace(s, "_")

								output = str(index) + t + image.replace(n,"") + t + page + t + "-"
								output_ = output + n
								f.write(output_)
								#print (output)
							except:
								output = str(index) + t + image + t + page + t + "error_1"
								print(output)
								pass
				except:
					output = str(index) #+ t + url + t + "error_2"
					print(output)
					pass

				try:
					url = "https://commons.wikimedia.org/wiki/" + image.replace("?","%3F")
					html = urlopen(url) 
					bsObj = BeautifulSoup(html,"html.parser")
					#print(bsObj)

					other_data = bsObj.find("div",{"id":"mw-imagepage-section-globalusage"}).find("ul")
					#print(other_data)

					for item in other_data.findAll("li"):
						lang = item.get("class",[])
						lang = str(lang).replace("[u'","").replace("']","")
						pages = item.findAll("li")
						#print(lang)

						for page in pages:
							try:
								page = page.get_text()

								output = str(index) + t + image.replace(n,"") + t + page + t + str(lang)
								output_ = output + n
								f.write(output_)
							except:
								output = str(index) + t + image.replace(n,"") + t + page + t + str(lang) + "error_3"
								print(output)
								pass
					print(index)
				except:
					output = str(index) #+ t + url + t + "error_4"
					print(output)
					pass
	time()

def get_img_typology(file):
	f_out = folder + "/typology" + ".tsv"

	url = "https://commons.wikimedia.org/wiki/" + file
	html = urlopen(url) 
	bsObj = BeautifulSoup(html,"html.parser")
	#print bsObj

	with open(f_out, "a") as f:
		raw_data = bsObj.find("table",{"id":"mw_metadata"}).find("tr",{"class":"exif-make"}).find("td")

		fil = file.replace(s,"_").replace(n,"")
		# header = file,size,user

		for item in raw_data:
			try:
				tex = item.get_text().replace(s, "_")
				text = tex.replace(n," ")

				output = fil + t + text
				output_ = output + n

				f.write(output_)
				#print(output)
			
			except:
				print(url)
				pass

def get_list(tsv_list):
	file = folder + "/" + tsv_list + ".tsv"
	index = 0

	time()
	
	with open(file, "rb") as in_file:
		#in_file = csv.reader(in_file, delimiter = t)
		filecontent = [line for line in in_file]

		for image in filecontent:
			index += 1

			try:
				#i = ", ".join(image)
				img = str(image)
				#print (img)

				# get_use(img,"commons") # commons other
				#get_img_typology(img)
				get_original_img_size(img,index)
				print(str(index))

			except:
				print (str(index))
				pass

# -----------------------------------
# Launch scripts

get_original_img_size("test/test") # test_2 eth_files_list
#get_usage("test/test_2") # eth_files_list test

#get_usage("Mona_Lisa,_by_Leonardo_da_Vinci,_from_C2RMF_retouched.jpg","others")  #commons others
#get_list("data/raw/20170407_a_Media_contributed_by_the_ETH-Bibliothek") # test/test data/raw/20170407_a_Media_contributed_by_the_ETH-Bibliothek


