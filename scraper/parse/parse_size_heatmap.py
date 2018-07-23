#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Create an heatmap

import os					# get file path
import csv					# read csv file
import sys					# reset file encoding

# -----------------------------------
# utilities

reload(sys)
sys.setdefaultencoding("utf-8")

folder = os.path.dirname(os.path.realpath(__file__))
t = "\t"
n = "\n"
s = " "

# -----------------------------------
# scripts 

def size_heatmap(f_name,block_size):

	func = "size-heatmap"
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_" + func + "-output.tsv" 
	# f_err = folder + "/data/" + f_name + "_" + func + "-errors.tsv" 
	
	with open(f_in, "r") as f1:
		with open(f_out, "a") as f2:
			# with open(f_err, "w") as f3:

			tsv_file = csv.reader(f1, delimiter=t)

			for item in tsv_file:
				width = item[4]
				height = item[5]

				new_w = int(width) / block_size
				new_h = int(height) / block_size 
				w_h = str(new_w) + "_" + str(new_h)

				output =  str(new_w) + t + str(new_h) + t + w_h
				f2.write(output + n)
				print(output)


# -----------------------------------
# Launch scripts 

size_heatmap("test",500);

