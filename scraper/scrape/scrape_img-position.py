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
import codecs
import linecache
# import urllib.parse


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

w_rev_limit = 1 # max 50
w_rev_api = ".wikipedia.org/w/api.php?action=parse&format=json&page=" # action=query (json) action=parse(html) &format=json
# w_prop = "&prop=revisions&rvprop=timestamp|user|comment|size|content&rvdir=older&rvlimit=" + str(w_rev_limit)

c_rev_limit = 1 # max 50
c_rev_api = "https://commons.wikimedia.org/w/api.php?action=parse&format=json&page=" #+ str(c_rev_limit)
# c_revisions = c_api + "&prop=revisions&rvprop=timestamp|user|comment|size|content&rvdir=newer&titles="

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

def clean_url_c(title):
	replace_01 = "ü"

	clean = title \
		.replace(replace_01,"%C3%BC")

	return clean

def whatisthis(s):
    if isinstance(s, str):
        print "ordinary string"
    elif isinstance(s, unicode):
        print "unicode string"
    else:
        print "not a string"

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)



# print(whatisthis("_Boden-Inlandfl%C3%BCge-LBS_MH05-72-08.tiff/lossy-page1-180px-Dornier_Do_K_ETH-BIB-Flugzeug_am_Boden-Inlandfl%C3%BCge-LBS_MH05-72-08.tiff.jpg 1.5x,"))

# -----------------------------------
# Script

# find string position in string
def find_str_a(s, char):
    index = 0
    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index+len(char)] == char:
                    return index
            index += 1
    return -1

def find_str_b(full, sub):
    index = 0
    sub_index = 0
    position = -1
    for ch_i,ch_f in enumerate(full) :
        if ch_f.lower() != sub[sub_index].lower():
            position = -1
            sub_index = 0
        if ch_f.lower() == sub[sub_index].lower():
            if sub_index == 0 :
                position = ch_i

            if (len(sub) - 1) <= sub_index :
                break
            else:
                sub_index += 1

    return position

# Wikipedia revisions
def get_img_position_w(f_name):

	func = "wiki_img_position"
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_" + func + "-output.tsv" 
	f_err = folder + "/data/" + f_name + "_" + func + "-errors.tsv" 
	print(func)

	with open(f_in, "r") as f1: # codecs.open(f_in, "r", "utf-8") 
		with open(f_out, "a") as f2:
			with open(f_err, "a") as f3:

				tsv_file = csv.reader(f1, delimiter=t)

				for row in tsv_file:
					id_file = row[0]
					file = row[1]
					outbound = row[2]
					link = row[3]
					page_lang = row[4]
					page_name = row[5]
					page_typo = row[6]
					# print(link + t + page_typo)

					index += 1
					file_clean = file.replace("File:","").replace(s,"_") #.replace('"',"\"") # .replace("_",s)

					def get_data(request):
						try:
							response = urlopen(request).read()
							data = json.loads(response)
							# print(data)

							for x in data.values():
								try:
									page = x["title"]
									content = x["text"]["*"]
									# print(content)

									my_file = urllib.quote_plus(file_clean) # unicode(file_clean, "utf-8") #urllib.quote_plus(file_clean.encode("utf-8")) # clean_url_c(file_clean.decode("utf-8")) # clean_url_a(file_clean) unicode(file_clean, encoding="utf-8") #
									my_content = content.encode("utf-8") #content.encode("utf-8") # clean_url_a(content) unicode(content, encoding="utf-8") # 

									page_length = len(content)
									img_position = find_str_a(my_content, my_file)
									img_position_relative = (img_position*100)/float(page_length)

									if (img_position != -1):
										output = str(id_file) + t + \
											file + t + \
											page + t + \
											page_lang + t + \
											page_typo + t + \
											str(page_length) + t + \
											str(img_position) + t + \
											str(img_position_relative)
										print(str(id_file))
										f2.write(output + n)
									else:
										output = str(id_file) + t + request + t + file
										print(output)
										f3.write(output + n)
													
								except:
									PrintException()
									output = str(id_file) + t + request + t + file_clean + t + "error_1"
									# print(output)
									f3.write(output + n)
									pass

						except:
							PrintException()
							output = str(id_file) + t + request + t + file_clean + t + "error_0"
							# print(output)
							f3.write(output + n)
							pass

					request = "https://" + page_lang + w_rev_api + page_name				
					get_data(request)

# Commons revisions
def get_img_position_c(f_name):

	func = "commons_img_position"
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_" + func + "-output.tsv" 
	f_err = folder + "/data/" + f_name + "_" + func + "-errors.tsv" 
	print(func)

	# f = codecs.open("suess_sweet.txt", "r", )    # suess_sweet.txt file contains two

	with open(f_in, "r") as f1: # codecs.open(f_in, "r", "utf-8") 
		with open(f_out, "a") as f2:
			with open(f_err, "a") as f3:

				tsv_file = csv.reader(f1, delimiter=t)

				for row in tsv_file:
					id_file = row[0]
					file = row[1]
					outbound = row[2]
					link = row[3]
					page_lang = row[4]
					page_name = row[5]
					page_typo = row[6]
					# print(link + t + page_typo)

					index += 1
					file_clean = file.replace("File:","").replace(s,"_") #.replace('"',"\"") # .replace("_",s)

					def get_data(request):
						try:
							response = urlopen(request).read()
							data = json.loads(response)
							# print(data)

							for x in data.values():
								try:
									page = x["title"]
									content = x["text"]["*"]
									# print(content)

									my_file = urllib.quote_plus(file_clean) # unicode(file_clean, "utf-8") #urllib.quote_plus(file_clean.encode("utf-8")) # clean_url_c(file_clean.decode("utf-8")) # clean_url_a(file_clean) unicode(file_clean, encoding="utf-8") #
									my_content = content.encode("utf-8") #content.encode("utf-8") # clean_url_a(content) unicode(content, encoding="utf-8") # 

									page_length = len(content)
									img_position = find_str_a(my_content, my_file)
									img_position_relative = (img_position*100)/float(page_length)

									if (img_position != -1):
										output = str(id_file) + t + \
											file + t + \
											page + t + \
											page_lang + t + \
											page_typo + t + \
											str(page_length) + t + \
											str(img_position) + t + \
											str(img_position_relative)
										print(str(id_file))
										f2.write(output + n)
									else:
										output = str(id_file) + t + request + t + file
										print(output)
										f3.write(output + n)	
										f2.write(output + n)	
								except:
									PrintException()
									output = str(id_file) + t + request + t + file_clean + t + "error_1"
									# print(output)
									f3.write(output + n)
									f2.write(output + n)
									pass

						except:
							PrintException()
							output = str(id_file) + t + request + t + file_clean + t + "error_0"
							# print(output)
							f3.write(output + n)
							f2.write(output + n)
							pass

					request = c_rev_api + page_name	
					# print(request)			
					get_data(request)

# -----------------------------------
# Launch script

# get_img_position_w("w_pages_using_files") #w_pages_using_files test
get_img_position_c("c_pages_using_files") #c_pages_using_files test

