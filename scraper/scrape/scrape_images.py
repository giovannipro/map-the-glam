#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Scrape data and open web pages

import os						# get file path
import webbrowser				# open webpages
import time		     			# get unix code
import datetime					# convert in unix timestamp
import urllib, json, io			# read json
from urllib import urlopen		# open file
import sys						# reset file encoding
import datetime					# print time
import csv						# read csv
import re						# replace all occurrences
from bs4 import BeautifulSoup	# parse html

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


# -----------------------------------
# API

commons = "https://commons.wikimedia.org/wiki/"

# -----------------------------------
# scripts

def scrape_image(f_name,start_id):
	func = "scrape_image"
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_err = folder + "/data/" + f_name + "_" + func + "-errors.tsv" 
	
	with open(f_in, "r") as f1:
		with open(f_err, "w+") as f2:

			tsv_file = csv.reader(f1, delimiter=t)

			for file in tsv_file:
				index += 1
				file_id = file[0]
				file_name = file[1]

				url = commons + file_name

				if (index >= start_id):
					# print (url)

					try:
						html = urlopen(url) 
						bsObj = BeautifulSoup(html,"html.parser")

						# img_url = bsObj.find("div",{"id":"file"}).find("a")['href'] # max size
						img_url = bsObj.find("div",{"id":"file"}).find("img")["src"]
						
						fil = file_id + "_" + file_name.replace("File:","")
						destination = "Desktop/eth-images/" + fil
						
						urllib.urlretrieve(img_url,destination)
						print(file_id)
						
					except Exception as e:
						output = str(file_id) + t + url
						print(output)
						f2.write(output + n)
						pass

def test(n):
	for a in range(n):
		print a

# -----------------------------------
# Launch scripts

scrape_image("test",0)  # test_data test

# >>> clean url


