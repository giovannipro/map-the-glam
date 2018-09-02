#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os					# get file path
import csv					# read csv file
import sys					# reset file encoding
import operator
from operator import itemgetter
import pandas as pd
import numpy as np
import re

# -----------------------------------
# Utilities

reload(sys)
sys.setdefaultencoding("utf-8")

folder = os.path.dirname(os.path.realpath(__file__))
t = "\t"
n = "\n"
s = " "
com = ","
# test = t + "test"

# -----------------------------------
# Script

def img_spread(f_name):

	func = "img_spread"
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_" + func + "-output.tsv" 
	f_err = folder + "/data/" + f_name + "_" + func + "-errors.tsv" 
	
	# dataset already in descending order of revision_date

	with open(f_in, "r") as f1:
		with open(f_out, "a") as f2:
			# with open(f_err, "a") as f3:

			# data = pd.read_csv(f1, \
			# 	names=["_id_file","file_name","page_lang","page_typology","page_link","revision_date","img_present","user","page_size"], \
			# 	sep=t, header=0, error_bad_lines=False)

			# data.sort_values(["revision_date","page_typology"], ascending=[True,True]) # "page_typology"

			# test_1 = data["revision_date"]
			# test_2 = data["page_typology"]
			# # print(test_1 + t + test_2) 
			# print(data.loc[:,"revision_date"]) # row,column
			
			# lines = f1.readlines()
			lines = csv.reader(f1, delimiter=t)
			sorted_tsv_a = sorted(lines, key = operator.itemgetter(5))
			# sorted_tsv_b = sorted(sorted_tsv_a, key = operator.itemgetter(5))
			# sorted_tsv = sorted(lines, key=itemgetter(3,5))
			# list1 = sorted(csv1, key=operator.itemgetter(1, 2))

			# date_sorted_tsv = sorted(lines, key=itemgetter(5))
			# pageType_sorted_tsv = sorted(date_sorted_tsv, key=itemgetter(3))

			date = "2000-01";
			new_date = "";
			new_page = "";
			new_file = "";
			new_img_present = "False";

			art_p = 0;
			usr_p = 0;
			wik_p = 0;
			dis_p = 0;

			de = 0;
			fr = 0;
			en = 0;
			es = 0;
			it = 0;
			fa = 0;
			ar = 0;
			pt = 0;
			ru = 0;
			nl = 0;
			other_lang = 0;
			
			for row in sorted_tsv_a:
				id_file = row[0]
				file = row[1]
				page_lang = row[2]
				page_typology = row[3]
				page_link = row[4]
				revision_date = row[5]
				img_present = row[6]
				user = row[7]
				page_size = row[8]

				date = revision_date[0:7]
				# test = date + t + revision_date + t + page_typology
				# print(test)
				
				# Wikipedia - page_typology
				if (img_present == "True"):
					# if (new_page != page_link):
					if (img_present != new_img_present):	
						if (page_typology == "article/to_check"):
							art_p += 1
						elif (page_typology == "user_page"):
							usr_p += 1
						elif (page_typology == "wikipedia_page"):
							wik_p += 1
						else:
							dis_p += 1
				# else:
				# 	if (img_present != new_img_present):	
				# 		if (page_typology == "article/to_check"):
				# 			art_p -= 1
				# 		elif (page_typology == "user_page"):
				# 			usr_p -= 1
				# 		elif (page_typology == "wikipedia_page"):
				# 			wik_p -= 1
				# 		else:
				# 			dis_p -= 1

				# Wikipedia - page_lang
				if (img_present == "True"):
					if (img_present != new_img_present):	
						if (page_lang == "de"):
							de += 1
						elif (page_lang == "fr"):
							fr += 1
						elif (page_lang == "en"):
							en += 1
						elif (page_lang == "es"):
							es += 1
						elif (page_lang == "it"):
							it += 1
						elif (page_lang == "fa"):
							fa += 1
						elif (page_lang == "ar"):
							ar += 1
						elif (page_lang == "pt"):
							pt += 1
						elif (page_lang == "ru"):
							ru += 1
						elif (page_lang == "nl"):
							nl += 1
						else:
							other_lang += 1
		

				if new_date != date:
					output_w_page_typology = date + t + str(art_p) + t + str(usr_p) + t + str(wik_p) + t + str(dis_p)
					output_w_page_lang = date + t + \
						str(de) + t + \
						str(fr) + t + \
						str(en) + t + \
						str(es) + t + \
						str(it) + t + \
						str(fa) + t + \
						str(ar) + t + \
						str(pt) + t + \
						str(ru) + t + \
						str(nl) + t + \
						str(other_lang)

					print(output_w_page_lang)
					f2.write(output_user + n)

				# else:
				# 	print(date + t + str(art_p) + t + page_link)

				new_date = date

def img_spread_c(f_name):

	func = "img_spread"
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_" + func + "-output.tsv" 
	f_err = folder + "/data/" + f_name + "_" + func + "-errors.tsv" 
	# dataset in descending order of revision_date

	with open(f_in, "r") as f1:
		with open(f_out, "a") as f2:

			lines = csv.reader(f1, delimiter=t)
			sorted_tsv_a = sorted(lines, key = operator.itemgetter(4))

			date = "2000-01";
			date = ""
			new_date = "";
			new_page = "";
			new_file = "";
			new_img_present = "False";

			art_p = 0;
			cat_p = 0;
			fil_p = 0;
			usr_p = 0;
			wik_p = 0;
			
			for row in sorted_tsv_a:
				id_file = row[0]
				file = row[1]
				page_typology = row[2]
				page_link = row[3]
				revision_date = row[4]
				img_present = row[5]
				user = row[6]
				page_size = row[7]
				# print(row)

				date = revision_date[0:7]

				if (img_present == "True"):
					# if (new_page != page_link):
					if (img_present != new_img_present):	
						if (page_typology == "article/to_check"):
							art_p += 1
						elif (page_typology == "category"):
							cat_p += 1
						elif (page_typology == "file"):
							fil_p += 1
						elif (page_typology == "user_page"):
							usr_p += 1
						elif (page_typology == "wikiproject"):
							wik_p += 1
						# else:
						# 	dis_p += 1
						# print(page_typology)

				if new_date != date:
					output = date + t + \
						str(art_p) + t + \
						str(cat_p) + t + \
						str(fil_p) + t + \
						str(usr_p) + t + \
						str(wik_p)

					print(output)
					# f2.write(output + n)
				# else:
				# 	output = date + t + page_link
				# 	print(output)
				
				new_date = date

def get_user_stream(f_name):

	func = "user_stream"
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_" + func + "-output.tsv" 
	# f_err = folder + "/data/" + f_name + "_" + func + "-errors.tsv" 

	reg = 0;
	ann = 0;
	bot = 0;

	new_page_link = "";
	new_date = "";
	new_user = "";

	with open(f_in, "r") as f1:
		with open(f_out, "a") as f2:

			lines = csv.reader(f1, delimiter=t)
			sorted_tsv_a = sorted(lines, key = operator.itemgetter(4))

			# tsv_file = csv.reader(f1, delimiter=t)

			for row in sorted_tsv_a:
				id_file = row[0]
				page_link = row[3] # 4
				revision_date = row[4] # 5
				img_present = row[5] # 6
				user = row[6] # 7

				date = revision_date[0:7]

				anon_1 = re.compile(r"[0-9]*\.[0-9]*")
				anon_2 = re.compile(r"[0-9]*:[0-9]*")

				if (img_present == "True"):
					if (page_link != new_page_link):
						if (user != new_user):
							if "bot" in user or "Bot" in user or "BOT" in user :
								# output = "bot" + t + user 
								bot += 1
							elif anon_1.search(user) or anon_2.search(user):
								# output = "ann" + t + user 
								ann += 1
							else:
								# output = "reg" + t + user
								reg += 1
							# print date + t + id_file + t + page_link + t + output
						
						new_user = user
					new_page_link = page_link
				# else:
				
				if new_date != date:
					output = date + t + str(reg) + t + str(ann) + t + str(bot) 
					print(output)
					f2.write(output + n)

					reg = 0;
					ann = 0;
					bot = 0;
				# else:
				# 	output = date + t + str(reg) + t + str(ann) + t + str(bot) + t + "<<<" 
				# 	print(output)

				new_date = date


def check_user_typology(f_name):

	func = "user_typology"
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_" + func + "-output.tsv" 
	# f_err = folder + "/data/" + f_name + "_" + func + "-errors.tsv" 

	with open(f_in, "r") as f1:
		with open(f_out, "a") as f2:
			# with open(f_err, "a") as f3:

			tsv_file = csv.reader(f1, delimiter=t)

			for item in tsv_file:
				user = item[7]

				anon_1 = re.compile(r"[0-9]*\.[0-9]*")
				anon_2 = re.compile(r"[0-9]*:[0-9]*")

				if "bot" in user or "Bot" in user or "BOT" in user :
					output = "bot" + t + user 
				elif anon_1.search(user) or anon_2.search(user):
					output = "ann" + t + user 
				else:
					output = "reg" + t + user
		
				print(output)
				f2.write(output + n)


# -----------------------------------
# Launch scripts

# img_spread_w("w_revisions")
# img_spread_c("c_revisions")

get_user_stream("c_revisions") # c_revisions w_revisions w_revisions_test

# check_user_typology("w_revisions")