#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Scrape images

import glob, os						# get file path
import sys							# reset file encoding
import webbrowser					# open webpages
import urllib, json, io				# read json
from urllib import urlopen			# open file
from bs4 import BeautifulSoup		# parse html
import PIL
from PIL import Image				# scale image

reload(sys)
sys.setdefaultencoding("utf-8")

# -----------------------------------
# Utilities

folder = os.path.dirname(os.path.realpath(__file__))
t = "\t"
n = "\n"
s = " "

# -----------------------------------
# Main variables

commons = "https://commons.wikimedia.org/wiki/File:"
basewidth = 500

# -----------------------------------
# Script

def get_images(img_list,limit):

	in_file = folder + "/" + img_list + ".tsv"
	output = folder + "/images"

	with open(in_file, "rb") as f:
		filecontent = [line for line in f]
		index = 0

		for img in filecontent:
			index += 1
			image = img.replace("\n\n", "\n").replace("File:","")

			try:

				if index < (limit + 1):
					url = commons + image
					html = urlopen(url) 
					bsObj = BeautifulSoup(html,"html.parser")

					raw_data = bsObj.find("div",{"id":"file"}).find("a")
					link = raw_data['href']

					destination = output + "/" + image
					
					urllib.urlretrieve(link,destination)
					print url

			except:
				print("error: " + str(url))
				pass

def scale_images(basewidth):

	my_folder = "/images"

	for file in os.listdir(folder + my_folder):
		try:
			f = folder + my_folder + "/" + file

			#if f.endswith(".tif"):
			if f.find(".tif"):
				print(f)

				img_original = Image.open(f)
				wpercent = (basewidth/float(img_original.size[0]))
				hsize = int((float(img_original.size[1])*float(wpercent)))
				img_new = img_original.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
				img.save(image_new) 
			else:
				print f

		except:
			print(f)
			pass

get_images("test/eth_files_list",120)
#scale_images(500)


