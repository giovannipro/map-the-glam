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
com = ","
test = t + "test"

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

'''
def count_co_occ():

	cat = ["cat_a","cat_b","cat_c"]

	file = [
		{"cat_a": ["file_1"]},
		{"cat_b": ["file_1","file_2"]},
		{"cat_c": ["file_1","file_2"]}
	]

	file_1 = [
		["cat_a", "file_1"],
		["cat_b", "file_2"]
	]
	
	for c in cat:
		category_1 = c
		weight = 0
		#print(category_1)
		
		for f in file_1:
			category_2 = f[0]
			f_1 = f[1]
			#print(category_1)

			if (category_1 == category_2):
				weight += 1
			# else:
			# 	print("error")
			
			output = category_1 + t + category_2 + t + str(weight)
			
			print output

'''

def count_co_occ_1():

	cat_1_list = ["cat_a","cat_b"]

	file_list = [
		  {
		    "file": "file_1",
		    "cat": [
		      "cat_a",
		    ]
		  },
		  {
		    "file": "file_2",
		    "cat": [
		      "cat_b",
		    ]
		  }
		]

	for cat_1 in cat_1_list:
		#file_index = 0

		for f in file_list:
			f_1 = f["file"]
			cat_2_list = f["cat"]
			weight = 0
			#file_index += 1

			'''
			for cat_2 in cat_2_list:
				print(cat_2)

				#if (cat_1 != cat_2): # and file_index != 0
				if cat_2 != cat_1:
					weight += 1
					
					#if cat_1 == cat_2:
					output = f_1 + t + cat_1 + t + cat_2 + t + str(weight) 
					#else:
					#output = f_1 + t + cat_1 + t + cat_2 + t + str(weight)
					
					print(output)
			'''
def count_co_occ_2():

	edges = ["cat_a","cat_b"]

	file_list = [
		  {
		    "file": "file_1",
		    "cat": [
		      "cat_a"
		    ]
		  },
		  {
		    "file": "file_2",
		    "cat": [
		      "cat_a",
		      "cat_b"
		    ]
		  }
		]

	for f in file_list:
		file = f["file"]
		cat = f["cat"]
		weight = 0
		index = 0

		for edge in edges:

			if edge in cat:
				weight += 1
				w = str(weight)
				output = edge + t + file + " in"

			else:
				weight += 0
				w = str(weight)
				output = edge + t + file + " no"


			print(output)



		'''

		for c in cat:
			#print (c)

			# index += 1
			# print index

			for edge in edges:

				if edge != c:
					weight += 1
					w = str(weight)
					print file + t + c + t + edge + t + w 
				# else:
				# 	weight += 0
				# 	w = str(weight)
				# 	print file + t + c + t + edge + t + w + " no"
				# 	#print("no")

		for edge in edges:
			#print edge
			index += 1

			for c in cat:
				#print str(index) + "-" + c
			
				if c != edge:
					weight += 1
					print("no-" + c + "-" + edge + str(weight))
				else:
					print("si-" + c + "-" + edge + str(weight))
				
		'''

def count_co_occ_3():

	edges = ["cat_a","cat_b"]

	file_list = [
		  {
		    "file": "file_1",
		    "cat": [
		      "cat_a"
		    ]
		  },
		  {
		    "file": "file_2",
		    "cat": [
		      "cat_a",
		      "cat_b"
		    ]
		  }
		]


	for edge in edges:
		weight = 0

		for x in edges:
			#print x + t + edge

			for f in file_list:
				file = f["file"]
				cat = f["cat"]

				for c in cat:

					if c != edge:
						weight += 1
					# else:
					# 	print "no"

			if edge != c:
				w = str(weight)
				print edge + t + c + t + w + test


	'''
	index = 0
	for f in file_list:
		file = f["file"]
		cat = f["cat"]
		index += 1
		print index

		for c in cat:



		# for c in cat:

		# 	for edge in edges:

		# 		if c in edge:
		# 			print c 

	'''


def count_co_occ_4():

	edges = ["cat_a","cat_b"]

	file_list = [
		  {
		    "file": "file_1",
		    "cat": [
		    "cat_a",
		      "cat_b"
		    ]
		  },
		  {
		    "file": "file_2",
		    "cat": [
		      "cat_a",
		      "cat_b"
		    ]
		  }
		]

	index = 0
	output = []

	for f in file_list:
		file = f["file"]
		cat = f["cat"]
		
		index += 1
		i = str(index)

		for edge in edges:
			weight = 0

			for c in cat:
	
				if edge != c:
					weight += 1
				# else:
				# 	weight += 50


				if edge != c:
					w = str(weight)
					out = edge + t + c + t + w + t + i
					#output.append([out])

					print out
	
def count_co_occ_5():

	edges = ["cat_a","cat_b"]
	files = ["file_1","file_2"]

	file_list = [
		  {
		    "file": "file_1",
		    "cat": [
		      "cat_a"
		    ]
		  },
		  {
		    "file": "file_2",
		    "cat": [
		      "cat_b"
		    ]
		  }
		]

	for f in file_list:
		file = f["file"]
		cat = f["cat"]	

		for c in cat:

			for edge in edges:
				#print file
				weight = 0

				if edge in cat:
					weight += 1
					w = str(weight)
				
				if edge != c:
					print file + t + edge + t + c + t + w
				# else:
				# 	print file + t + edge + t + c + t + w + test

			# for c in cat:
			# 	print edge + t + c		




# -----------------------------------
# Launch scripts

# edges("to_gephi_test") # to_gephi_test eth-biblioteck-uploads2016
# nodes("eth-biblioteck-uploads2016")

count_co_occ_5()


