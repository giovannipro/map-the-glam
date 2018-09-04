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

# -----------------------------------
# Script

def parse_pv_date(f_name):

	func = "parse_pv"
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_" + func + "-output.tsv" 

	with open(f_in, "r") as f1:
		with open(f_out, "a") as f2:

			lines = csv.reader(f1, delimiter=t)
			sorted_tsv_a = sorted(lines, key = operator.itemgetter(1))

			# data = pd.read_csv(f1, names=["id","file","outbound","link","page","pagetype"], sep=t, header=1, error_bad_lines=False)

			# a = data.groupby(["file"])["outbound"].count() #.sum() #.groups.keys() #.groups["2014-11"] #"outbound"]) #.size()
			# a = data.groupby(["file","outbound"]).count()  #.count()  # ["file"]
			# print a

			# new_file = ""
			# w = 0
			# c = 0
			# o = 0

			for row in sorted_tsv_a:
				id_file = row[0]
				file = row[1]
				link = row[2]
				lang = row[3]
				page_typo = row[4]
				date = row[5]
				pv = row[6]

				year = date[0:4]
				month = date[4:6]
				day = date[6:8]

				parsed_date = year + "-" + month + "-" + day
				project = "wikipedia"

				output = id_file + t + \
					file + t + \
					link + t + \
					lang + t + \
					project + t + \
					page_typo  + t + \
					parsed_date + t + \
					pv
				print(id_file)
				f2.write(output + n)

			# 	data = []
			# 	if outbound == "commons":
			# 		c += 1
			# 	elif outbound == "wikipedia":
			# 		w += 1
			# 	else:
			# 		o += 1
			# 	output = str(id_file) + t + file + t + str(w) + t + str(c) + t + str(o)
			# 	# data.append(output)

			# 	if new_file != file:
			# 		print(output)
			# 		f2.write(output + n)
			# 		w = 0
			# 		c = 0
			# 		o = 0
			# 	new_file = file

# -----------------------------------
# Launch scripts


parse_pv_date("w_pv")
