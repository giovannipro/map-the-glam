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

def get_image_usage(f_name):

	func = "image_usage"
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

			new_file = ""
			w = 0
			c = 0
			o = 0

			for row in sorted_tsv_a:
				id_file = row[0]
				file = row[1]
				outbound = row[2]

				data = []
				if outbound == "commons":
					c += 1
				elif outbound == "wikipedia":
					w += 1
				else:
					o += 1
				output = str(id_file) + t + file + t + str(w) + t + str(c) + t + str(o)
				# data.append(output)

				if new_file != file:
					print(output)
					f2.write(output + n)
					w = 0
					c = 0
					o = 0
				new_file = file

# -----------------------------------
# Launch scripts


get_image_usage("all_image_usage")
