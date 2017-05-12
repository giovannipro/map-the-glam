#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Get revisions

import os							# get file path
import sys							# reset file encoding
import webbrowser					# open webpages
import urllib, json, io				# read json
from urllib import urlopen			# open file
import datetime						# print time
import csv							# read csv

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

commons_api = "https://commons.wikimedia.org/w/api.php?action=query&format=json"
wikipedia_api = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles="

w_prop = "&rvprop=timestamp|user|ids|comment|size|comment|content"
commons_revisions = commons_api + "&prop=revisions&rvprop=timestamp|user|comment|content&titles="
limit = 50

# -----------------------------------
# Script

def time():
	my_format = "%d %m %Y %I:%M%p" 
	ts = datetime.datetime.utcnow().strftime(my_format)
	print(ts)

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

# Wikipedia revisions
def get_wiki_revisions(f_name): 
	time()

	f_in = folder + "/" + f_name + ".tsv"  # test / data
	f_out = folder + "/" + f_name + "-revisions_2.tsv" 

	with open(f_in, "r") as f1:
		with open(f_out, "w") as f2:

			tsvin = csv.reader(f1, delimiter = t)
			index = 0

			for row in tsvin:
				file = row[0]
				page = row[1]
				# print (file + t + page)

				request = wikipedia_api + page + w_prop + "&rvlimit=" + str(limit)
				print(request)

				response = urlopen(request).read()
				data = json.loads(response)
				#print(data)

				new_continue = data["continue"]["rvcontinue"]
				id_ = data["query"]["pages"].items()[0][0]
				revisions = data["query"]["pages"][id_]["revisions"]
				print (new_continue)

				# for r in revisions:
				# 	try:
				# 		revid = r["revid"]
				# 		user = r["user"]
				# 		timestamp = r["timestamp"]
				# 		size = r["size"]

				# 		output = timestamp + t + user + t + str(size)
				# 		print(output)
				# 	except:
				# 		print(request)
				# 		pass

				# if (new_continue != 0):
				# 	get_second_revisions(article,new_continue)

# Commons revisions
def get_commons_revisions(f_name):
	time()

	f_in = folder + "/" + f_name + ".tsv"  # test / data
	f_out = folder + "/" + f_name + "-revisions.tsv" 
	
	with open(f_in, "r") as f1:
		with open(f_out, "w") as f2:

			tsvin = csv.reader(f1, delimiter = t)
			index = 0

			for row in tsvin:
				file = row[0]
				page = row[1]
				# print (file + t + page)

				index += 1
				f = file.replace("_",s)

				request = commons_revisions + page

				response = urlopen(request).read()
				data = json.loads(response)
				
				for x in data["query"]["pages"]:
					_id = x
				
				for x in data["query"]["pages"].values():
					try:
						page = x["title"]
						revisions = x["revisions"]
						#print(revisions)
					except:
						output = request + t + file + t + "error_1"
						print(output)
						pass

				for y in revisions:
					user = y["user"]
					timestamp = y["timestamp"]
					content = y["*"]
					# print(content)

					#"a\x81b".decode("utf-8", "replace")
					content.replace('__TOC__',"")

					#a = "0xc3"
					#a.decode("utf-8","replace")
					#print(content)

					if (f in content or file in content):
						i = str(index)
						output = i + t + file + t + page + t + user + t + timestamp
						output_ = output + n
						
						f2.write(output_)
						print (i)
					else:
						output = request + t + file + t + "error_2"
						print(output)

# -----------------------------------
# Launch script

get_wiki_revisions("test/test")
#get_commons_revisions("data/raw/20170417_use_on_commons") # test/test

#get_revisions("Day_of_Reconciliation")
#get_revisions("Talk:Day_of_Reconciliation")



