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
import re						# replace all occurrences
import linecache

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

# w_prop = "&rvprop=timestamp|user|ids|comment|size|comment|content&rvstart=2001-00-01T00:00:00Z"
# w_rev_api = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles="
w_rev_limit = 50 # max 50
w_rev_api = ".wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles=" # action=query
w_prop = "&prop=revisions&rvprop=timestamp|user|comment|size|content&rvlimit=" + str(w_rev_limit) + "&rvdir=newer"

c_rev_limit = 50 # max 50
c_api = "https://commons.wikimedia.org/w/api.php?action=query&format=json&rvlimit=" + str(c_rev_limit)
c_revisions = c_api + "&prop=revisions&rvprop=timestamp|user|comment|size|content&rvdir=newer&titles="

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

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


# -----------------------------------
# Script

# Wikipedia revisions
def get_wikipedia_revisions(f_name):
	# time()

	func = "wiki_revisions"
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_" + func + "-output.tsv" 
	f_err = folder + "/data/" + f_name + "_" + func + "-errors.tsv" 
	print(func)

	with open(f_in, "r") as f1:
		with open(f_out, "a") as f2:
			with open(f_err, "a") as f3:

				tsv_file = csv.reader(f1, delimiter=t)

				for row in tsv_file:
					id_file = row[0]
					file = row[1]
					link = row[3]
					the_page = row[5]
					page_type = row[6]
					# lang = row[3].replace("//","").split(".")[0]
					lang = row[4]
					# print(lang)

					index += 1
					file_clean = file.replace("_",s).replace("File:","")

					# if ("User:" in the_page or "Benutzer:" in the_page or "Auteur:" in the_page or "Author:" in the_page or "%D9%85%D8%B3%D8%AA%D8%AE%D8%AF%D9%85:" in the_page or "Usuario:" in the_page or "Usuari:" in the_page or "Utilisateur:" in the_page or "Sablon:" in the_page):
					# 	page_type = "user_page"
					# elif ("Wikipedia:" in the_page or "Wikipédia:" in the_page):
					# 	page_type = "wikipedia_page"
					# elif ("Project:" in the_page):
					# 	page_type = "project"
					# elif ("Discussion:" in the_page or "Talk:" in the_page or "Diskussion:" in the_page):
					# 	page_type = "discussion"
					# elif ("Commons:WikiProject" in the_page):
					# 	page_type = "wikiproject"
					# elif ("Category" in the_page):
					# 	page_type = "category"
					# elif ("File:" in the_page):
					# 	page_type = "file"
					# elif ("wikidata.org/wiki/Q" in the_page):
					# 	page_type = "item"
					# elif ("Portal" in the_page):
					# 	page_type = "portal"
					# elif ("Grants:" in the_page or "Wikimedia " in the_page):
					# 	page_type = "other"
					# else:
					# 	page_type = "article/to_check"
					# output = id_file + t + page_type
					# f2.write(output + n)
					# print(index)

					# if "wikipedia" in link:
					# 	outbound = "wikipedia"
					# elif "wikidata" in link:
					# 	outbound = "wikidata"
					# elif "meta.wikimedia" in link:
					# 	outbound = "meta"
					# elif "wikibooks" in link:
					# 	outbound = "wikibooks"
					# else:
					# 	outbound = "to_check"
					# output = id_file + t + the_page + t + outbound
					# f2.write(output + n)
					# print(index)

					def get_data(request):
						try:
							response = urlopen(request).read()
							data = json.loads(response)
							# print(data)

							for x in data["query"]["pages"].values():
								try:
									page = x["title"]
									revisions = x["revisions"]
									# print(page)

									for y in revisions:
										try:
											user = y["user"]
											timestamp = y["timestamp"]
											size = y["size"]
											content = y["*"]

											if (file_clean in content or file in content):
												img = True
											else:
												img = False

											output = id_file + t + file_clean + t + lang + t + page_type + t + page + t + timestamp + t + str(img) + t + user + t + str(size) 
											# print(output)
											f2.write(output + n)
											
										except Exception as e:
											output = request + t + file_clean + t + page + t + "error_2"
											# print(e)
											f3.write(output + n)
											pass

								except Exception as e:
									output = request + t + file_clean + t + page + t + "error_1"
									# print(e)
									f3.write(output + n)
									pass

							try:
								new_rvcontinue = data["continue"]["rvcontinue"]
								if new_rvcontinue != 0: # and new_rvcontinue != rvcontinue:
									request = "https://" + lang + w_rev_api + page + w_prop + "&rvcontinue=" + str(new_rvcontinue)
									get_data(request)
								print(new_rvcontinue)
							except Exception as e:
								pass

						except Exception as e:
							print e
							output = request + t + "error_0"
							f3.write(output + n)
							pass

					rvcontinue = 0
					if rvcontinue != 0:
						request = "https://" + lang + w_rev_api + the_page + w_prop + "&rvcontinue=" + str(rvcontinue)
						get_data(request)
					else:
						request = "https://" + lang + w_rev_api + the_page + w_prop
						get_data(request)

					print(str(index) + t + str(rvcontinue))

# Commons revisions
def get_commons_revisions(f_name):
	# time()

	func = "commons_revisions"
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_" + func + "-output.tsv" 
	f_err = folder + "/data/" + f_name + "_" + func + "-errors.tsv" 
	print(func)

	with open(f_in, "r") as f1:
		with open(f_out, "a") as f2:
			with open(f_err, "a") as f3:

				tsv_file = csv.reader(f1, delimiter=t)

				for row in tsv_file:
					id_file = row[0]
					file = row[1]
					link = row[3]
					the_page = row[3]
					page_type = row[2]
					# print(page_type)

					index += 1
					file_clean = file.replace("_",s).replace("File:","")

					def get_data(request):
						try:
							response = urlopen(request).read()
							data = json.loads(response)
							# print(data)

							for x in data["query"]["pages"].values():
								try:
									page = x["title"]
									revisions = x["revisions"]
									# print(page)

									for y in revisions:
										try:
											user = y["user"]
											timestamp = y["timestamp"]
											size = y["size"]
											content = y["*"]

											if (file_clean in content or file in content):
												img = True
											else:
												img = False

											output = id_file + t + file_clean + t + t + page_type + t + page + t + timestamp + t + str(img) + t + user + t + str(size) 
											# print(output)
											f2.write(output + n)
											
										except Exception as e:
											PrintException()
											output = request + t + file_clean + t + page + t + "error_2"
											print(e)
											f3.write(output + n)
											pass

								except Exception as e:
									PrintException()
									output = request + t + file_clean + t + page + t + "error_1"
									# print(e)
									f3.write(output + n)
									pass

							try:
								new_rvcontinue = data["continue"]["rvcontinue"]
								if new_rvcontinue != 0: # and new_rvcontinue != rvcontinue:
									request = c_revisions + page + "&rvcontinue=" + str(new_rvcontinue)
									get_data(request)
								print(new_rvcontinue)
							except Exception as e:
								pass

						except Exception as e:
							# print e
							PrintException()
							output = request + t + "error_0"
							f3.write(output + n)
							pass

					rvcontinue = 0
					if rvcontinue != 0:
						request = c_revisions + the_page + "&rvcontinue=" + str(rvcontinue)
						get_data(request)
					else:
						request = c_revisions + the_page
						get_data(request)

					print(str(index) + t + str(rvcontinue))
					# print(request)

# file_features
def used_file_features(f_name,f_base):
	# time()

	func = "used_file_features"
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_" + func + "-output.tsv" 
	f_base = folder + "/data/" + f_base + ".tsv" 

	with open(f_in, "r") as f1:
		with open(f_out, "a") as f2:
			with open(f_base, "r") as f3:

				tsv_used_file = csv.reader(f1, delimiter=t)
				tsv_all_file = csv.reader(f3, delimiter=t)

				ids = []

				for row in tsv_used_file:
					id_file = row[0]
					ids.append(id_file)
				ids.sort()

				# print(ids)

				for file in tsv_all_file:
					id_ = file[0]
					a = file[1]
					b = file[2]
					c = file[3]
					d = file[4]
					e = file[5]
					f = file[6]
					g = file[7]
					h = file[8]
					i = file[9]

					if id_ in ids:
						output = id_ + t + \
							a + t + \
							b + t + \
							c + t + \
							d + t + \
							e + t + \
							f + t + \
							g + t + \
							h + t + \
							i
						print(id_)
						f2.write(output + n)

# clean file name
def clean_file_name(f_name):

	func = "clean_file_name"
	index = 0
	print(func)

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_" + func + "-output.tsv" 
	# f_base = folder + "/data/" + f_base + ".tsv" 

	with open(f_in, "r") as f1:
		with open(f_out, "a") as f2:
			# with open(f_base, "r") as f3:

				tsv_file = csv.reader(f1, delimiter=t)

				for row in tsv_file:
					id_ = row[0]
					name = row[1]

					name_clean = name.replace("File:","").replace("ETH-BIB-Zürich","").replace("ETH","").replace("H-","").replace("F-","").replace("AL-","").replace("MH--","").replace("ETH","").replace("-BIB-","").replace(".tif","").replace(".jpg","").replace("--","").replace("MH-","").replace("-LBS","")
					name_clean_1 = ''.join(i for i in name_clean if not i.isdigit())
					name_clean_2 = name_clean_1.split(",")[0] 

					output = id_ + t + name_clean_2
					print(output)
					f2.write(output + n)


# -----------------------------------
# Launch script

# get_wikipedia_revisions("test_revisions_w") 
get_commons_revisions("test_c")

# used_file_features("test_used_files","files_metadata")

# clean_file_name("file_name")
