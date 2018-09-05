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

def img_spread_w(f_name,project,get):

	func = "img_spread"
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_" + func + "_" + get + "-output.tsv" 
	f_err = folder + "/data/" + f_name + "_" + func + "_" + get + "-errors.tsv" 
	
	# dataset already in descending order of revision_date

	with open(f_in, "r") as f1:
		with open(f_out, "a") as f2:
			# with open(f_err, "a") as f3:
			
			lines = csv.reader(f1, delimiter=t)
			sorted_tsv_a = sorted(lines, key = operator.itemgetter(5,2,4,3)) # w 5,2,4,3

			date = "2000-01";
			new_date = "";
			new_page_link = "";
			new_page_id = "";
			new_file = "";
			new_size = "";
			new_img_present = "False";

			art_p = 0;
			usr_p = 0;
			wik_p = 0;
			dis_p = 0;

			artc_p = 0;
			catc_p = 0;
			filc_p = 0;
			usrc_p = 0;
			wikc_p = 0;

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

			pages_typo_w = [];
			pages_typo_c = [];
			pages_lang = [];
			
			last_cycle = len(sorted_tsv_a) - 1
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
				page_id = page_lang + "_" + page_link.replace(s,"_")
				page_extended_id = page_id + "_" + img_present

				test = date + t + page_extended_id
				# print(test)

				index += 1
				# print(str(last_cycle) + t + str(index))
				
				# Wikipedia - page_typology
				if (project == "w"):
					if (img_present == "True"):	
						if (page_id not in pages_typo_w):
							if (page_typology == "article/to_check"):
								art_p += 1
							elif (page_typology == "user_page"):
								usr_p += 1
							elif (page_typology == "wikipedia_page"):
								wik_p += 1
							else:
								dis_p += 1
							pages_typo_w.append(page_id)
					# else:
					# 	if (img_present == new_img_present and page_id in pages_lang):	
					# 		if (page_typology == "article/to_check"):
					# 			art_p -= 1
					# 		elif (page_typology == "user_page"):
					# 			usr_p -= 1
					# 		elif (page_typology == "wikipedia_page"):
					# 			wik_p -= 1
					# 		else:
					# 			dis_p -= 1
					# 		out = revision_date + t + page_lang + t + page_link + t + img_present + t + "<<<"
					# 		print(out)

				# Commons - page_typology
				if (project == "c"):
					if (img_present == "True"):
						if (page_id not in pages_typo_c):
						# if (img_present != new_img_present):
						# if (img_present == "True"):
							if (page_typology == "article/to_check"):
								artc_p += 1
							elif (page_typology == "category"):
								catc_p += 1
							elif (page_typology == "file"):
								filc_p += 1
							elif (page_typology == "user_page"):
								usrc_p += 1
							elif (page_typology == "wikiproject"):
								wikc_p += 1
							# print(page_extended_id + t + "<<<")
							pages_typo_c.append(page_id)
							# else:
							# 	print(page_extended_id)

				# Wikipedia - page_lang
				if (img_present == "True" and new_img_present != img_present):	
					if (page_id not in pages_lang):
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
						pages_lang.append(page_id)
						# out = revision_date + t + page_lang + t + page_link + t + img_present + t + "<<<"
						# print(out)
						# f2.write(out + n)
					# else:
					# 	if page_id not in excluded:
					# 		excluded.append(revision_date + t + page_id + t + img_present)
					# 	print(revision_date + t + page_id + t + img_present)

				output_w_page_typology = date + t + \
					str(art_p) + t + \
					str(usr_p) + t + \
					str(wik_p) + t + \
					str(dis_p)
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
				output_c_typology = date + t

				if new_date != date:
					if project == "w":
						if get == "typo":
							print(output_w_page_typology)
							f2.write(output_w_page_typology + n)
						elif get == "lang":
							print(output_w_page_lang)
							f2.write(output_w_page_lang + n)
					elif project == "c":
						output = date + t + \
							str(artc_p) + t + \
							str(catc_p) + t + \
							str(filc_p) + t + \
							str(usrc_p) + t + \
							str(wikc_p)
						print(output)
						f2.write(output + n)

				# else:
				# 	print(output_w_page_lang)			
					# print(date + t + str(art_p) + t + page_link)
					# print(output_w_page_lang)

				new_date = date
				new_page_link = page_link
				new_img_present = img_present
				new_file = file
				new_size = page_size
				new_page_id = page_id

			# index = 0
			# pages_sorted = sorted(pages, key = operator.itemgetter(0))
			# for a in pages_sorted:
			# 	index += 1
			# 	print(str(index) + t + a)

			# ind = 0
			# excluded_sorted = sorted(excluded, key = operator.itemgetter(0))
			# for a in excluded_sorted:
			# 	ind += 1
			# 	print(str(ind) + t + a)


# def img_spread_c(f_name):

# 	func = "img_spread"
# 	index = 0

# 	f_in = folder + "/data/" + f_name + ".tsv"
# 	f_out = folder + "/data/" + f_name + "_" + func + "-output.tsv" 
# 	f_err = folder + "/data/" + f_name + "_" + func + "-errors.tsv" 
# 	# dataset in descending order of revision_date

# 	with open(f_in, "r") as f1:
# 		with open(f_out, "a") as f2:

# 			lines = csv.reader(f1, delimiter=t)
# 			sorted_tsv_a = sorted(lines, key = operator.itemgetter(4))

# 			date = "2000-01";
# 			date = ""
# 			new_date = "";
# 			new_page = "";
# 			new_file = "";
# 			new_img_present = "False";

# 			art_p = 0;
# 			cat_p = 0;
# 			fil_p = 0;
# 			usr_p = 0;
# 			wik_p = 0;
			
# 			s = len(l) - 1
# 			for row in sorted_tsv_a:
# 				id_file = row[0]
# 				file = row[1]
# 				page_typology = row[2]
# 				page_link = row[3]
# 				revision_date = row[4]
# 				img_present = row[5]
# 				user = row[6]
# 				page_size = row[7]
# 				# print(row)

# 				date = revision_date[0:7]
# 				page_id = page_lang + "_" + page_link.replace(s,"_")
# 				page_extended_id = page_id + "_" + img_present

# 				if (img_present == "True"):
# 					# if (new_page != page_link):
# 					if (img_present != new_img_present):	
# 						if (page_typology == "article/to_check"):
# 							art_p += 1
# 						elif (page_typology == "category"):
# 							cat_p += 1
# 						elif (page_typology == "file"):
# 							fil_p += 1
# 						elif (page_typology == "user_page"):
# 							usr_p += 1
# 						elif (page_typology == "wikiproject"):
# 							wik_p += 1
# 						# else:
# 						# 	dis_p += 1
# 						# print(page_typology)

# 				if new_date != date:
# 					output = date + t + \
# 						str(art_p) + t + \
# 						str(cat_p) + t + \
# 						str(fil_p) + t + \
# 						str(usr_p) + t + \
# 						str(wik_p)

# 					# print(output)
# 					# f2.write(output + n)
# 				# else:
# 				# 	output = date + t + page_link
# 				# 	print(output)
				
# 				new_date = date

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
	new_img_present = "False";

	pages = [];

	with open(f_in, "r") as f1:
		with open(f_out, "a") as f2:

			lines = csv.reader(f1, delimiter=t)
			sorted_tsv_a = sorted(lines, key = operator.itemgetter(5,2,4,3)) # 4

			for row in sorted_tsv_a:
				id_file = row[0]
				page_lang = row[2]
				page_link = row[4]
				revision_date = row[5]
				img_present = row[6]
				user = row[7]

				date = revision_date[0:7]
				page_id = page_lang + "_" + page_link.replace(s,"_")
				page_extended_id = page_id + "_" + img_present

				anon_1 = re.compile(r"[0-9]*\.[0-9]*")
				anon_2 = re.compile(r"[0-9]*:[0-9]*")

				if (img_present == "True"):  
					if (page_id not in pages):
						# and img_present != new_img_present):
						# if (date != new_date):
							# if (page_link != new_page_link):
							# 	if (user != new_user):
						if "bot" in user or "Bot" in user or "BOT" in user or "BoT" in user:
							bot += 1
						elif anon_1.search(user) or anon_2.search(user):
							ann += 1
						else:
							reg += 1
						pages.append(page_id)
						out = date + t + page_id + t + user

				if new_date != date:
					output = date + t + str(reg) + t + str(ann) + t + str(bot) 
					print(output)
					f2.write(output + n)

					reg = 0;
					ann = 0;
					bot = 0;

				new_user = user
				new_page_link = page_link
				new_date = date
				new_img_present = img_present

			# index = 0
			# pages_sorted = sorted(pages, key = operator.itemgetter(0))
			# for a in pages_sorted:
			# 	index += 1
			# 	print(str(index) + t + a)

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

				if "bot" in user or "Bot" in user or "BOT" in user or "BoT" in user:
					output = "bot" + t + user 
				elif anon_1.search(user) or anon_2.search(user):
					output = "ann" + t + user 
				else:
					output = "reg" + t + user
		
				print(output)
				f2.write(output + n)


def count_file_per_page(f_name,project):

	func = "file_per_page"
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_" + func + "-output.tsv" 
	f_err = folder + "/data/" + f_name + "_" + func + "-errors.tsv" 
	
	# dataset already in descending order of revision_date

	new_page_link = ""
	new_file = ""

	with open(f_in, "r") as f1:
		with open(f_out, "a") as f2:
			# with open(f_err, "a") as f3:
			
			lines = csv.reader(f1, delimiter=t)
			sorted_tsv_a = sorted(lines, key = operator.itemgetter(2,4,1))
			
			count = 0;

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

				page_id = page_lang + "_" + page_link

				if new_file != file:
					count += 1
				
				output = page_id + t + page_lang + t + page_link + t + file + t + str(count)

				if new_page_link != page_link:
					print (output)
					count = 0;
					f2.write(output + n)

				# if img_present == "True" and 
				# if new_file != file:
				# print (output)


				new_file = file


# -----------------------------------
# Launch scripts

# img_spread_w("c_revisions","c","typo") #w_revisions test_page_spread  lang

# get_user_stream("c_revisions") # c_revisions w_revisions w_revisions_test

# check_user_typology("c_revisions")

count_file_per_page("c_revisions","c")