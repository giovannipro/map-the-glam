#! python
#! /usr/bin python
# Create file for Gephi

import os					# get file path
import csv					# read csv file
import sys					# reset file encoding

# -----------------------------------
# Utilities

reload(sys)
sys.setdefaultencoding("utf-8")

folder = os.path.dirname(os.path.realpath(__file__))
t = "\t"
n = "\n"
s = " "

# -----------------------------------
# Script

def tsv_to_csv(my_file):

	my_input = folder + "/data/" + my_file + ".tsv"
	output = folder + "/" + my_file + "_clean.tsv"

	with open(my_input, "rb") as in_file, open(output, 'wb') as out_file:
		in_file = csv.reader(in_file, delimiter = t)
		filecontents = [line for line in in_file]

		out_file = csv.writer(out_file, quotechar='', quoting=csv.QUOTE_NONE)
		out_file.writerows(filecontents)

def edges(my_file):

	file = folder + "/test/" + my_file + ".tsv"
	output = folder + "/" + my_file + "_edges.tsv"

	with open(file, "rb") as in_file, open(output, "wb") as out_file:  # , encoding="utf-8"
		in_file = csv.reader(in_file, delimiter = t)

		# for x in in_file:
		# 	title = x[0]
		# 	cat_ = x[2]

		# 	print(title)

		filecontents = [line for line in in_file]
		#print(filecontents)

		# for x in in_file:
		# 	title = x[0]
		# 	cat_ = x[2]

		# 	if title.strip():
		# 		categories = cat_.split("|")

		# 		for cat in categories:
		# 			final_output = title + t + cat + t + cat + n
		# 			out_file.write(final_output)
					#print(final_output)


		# filecontents[0][0] = "" # source
		# filecontents[0][2] = "" # target
		head = "source" + t + "target"+ t + "label" + n
		out_file.write(head)

		for row in filecontents:
			title = row[0]
			cat_ = row[2]
		
			if title.strip():
				categories = cat_.split("|")

				for cat in categories:
					final_output = title + t + cat + t + cat + n
					out_file.write(final_output)

def nodes(my_file):

	file = folder + "/test/" + my_file + ".tsv"
	output = folder + "/" + my_file + "_nodes.tsv"

	with open(file, "rt") as in_file, open(output, "wb") as out_file:
		in_file = csv.reader(in_file, delimiter = t)
		filecontents = [line for line in in_file]

		filecontents[0][0] = "" # source
		filecontents[0][2] = "" # target
		head = "id" + t + "label" + n
		out_file.write(head)

		_id = 0

		for row in filecontents:
			title = row[0]
			cat_ = row[2]

			if title.strip():
				categories = cat_.split("|")

				for cat in categories:
					final_output = cat + t + cat + n
					out_file.write(final_output)
								
				# _id += 1
				# row_id = str(_id)

				# final_output = title + t + title + n
				# out_file.write(final_output)

# -----------------------------------
# Launch scripts

edges("to_gephi_test") # to_gephi_test eth-biblioteck-uploads2016
#nodes("eth-biblioteck-uploads2016")
