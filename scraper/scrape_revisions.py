#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Get revisions

import os							# get file path
import sys							# reset file encoding
import webbrowser					# open webpages
import urllib, json, io				# read json
from urllib import urlopen			# open file

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

wikipedia_api = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles="
w_prop = "&rvprop=timestamp|user|ids|comment|size|comment|content"
limit = 50

# -----------------------------------
# Script


def get_second_revisions(article,cont):

	if cont == 0:
		request = wikipedia_api + article + w_prop + "&rvlimit=" + str(limit)
	else:
		request = wikipedia_api + article + w_prop + "&rvlimit=" + str(limit) + "&rvcontinue=" + str(cont)
	#print(request)

	response = urlopen(request).read()
	data = json.loads(response)
	#print(data)

	#new_continue = data["continue"]["rvcontinue"]
	id = data["query"]["pages"].items()[0][0]
	revisions = data["query"]["pages"][id]["revisions"]
	#print new_continue

	for r in revisions:
		try:
			revid = r["revid"]
			user = r["user"]
			timestamp = r["timestamp"]
			size = r["size"]

			output = timestamp + t + user + t + str(size)
			print(output)

		except:
			print(request)
			pass

	new_new_cont = data["continue"]["rvcontinue"]
	index = 0

	if (new_new_cont != 0 and new_new_cont != cont): 
		get_second_revisions(article,new_new_cont)
		index += 1
		#print(index)
	else:
		print("stop")

def get_revisions(article):
	
	request = wikipedia_api + article + w_prop + "&rvlimit=" + str(limit)
	print(request)

	response = urlopen(request).read()
	data = json.loads(response)
	#print(data)

	new_continue = data["continue"]["rvcontinue"]
	id = data["query"]["pages"].items()[0][0]
	revisions = data["query"]["pages"][id]["revisions"]
	#print (new_continue)

	for r in revisions:
		try:
			revid = r["revid"]
			user = r["user"]
			timestamp = r["timestamp"]
			size = r["size"]

			output = timestamp + t + user + t + str(size)
			print(output)
		except:
			print(request)
			pass

	if (new_continue != 0):
		get_second_revisions(article,new_continue)


# -----------------------------------
# Launch script
#get_revisions("Day_of_Reconciliation")
get_revisions("Talk:Day_of_Reconciliation")


