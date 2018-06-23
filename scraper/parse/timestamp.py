#! python
#! /usr/bin python
# Parse timestamp

import os					# get file path
import urllib, json, io		# read json
from urllib import urlopen	# open file
import sys					# reset file encoding
import csv					# read csv
import collections 			# count occurrences

from multiprocessing import Process

import pandas as pd
import numpy as np

reload(sys)
sys.setdefaultencoding("utf-8")

# -----------------------------------
# Utilities

folder = os.path.dirname(os.path.realpath(__file__))
t = "\t"
n = "\n"

def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)			        	
    return output

# -----------------------------------
# Scripts 

def timestamp(f_name):

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_output.tsv" 
	f_err = folder + "/data/" + f_name + "_error.tsv"

	with open(f_in, "r") as in_file:
		with open(f_out, "w") as f2, open(f_err, "w") as f3:

			data = pd.read_csv(in_file, names=["index","title","extension","timestamp","license","mediatype"], sep=t, header=1, error_bad_lines=False)
			# print data

			timestamp = data["timestamp"].str[0:7] 
			table_sum = data.groupby([timestamp,"license"]).size() #.agg({"0": np.sum})  # 'c': np.mean

			print table_sum

			for row in table_sum:
				print row

			# print table

			# print data["timestamp"].str[0:7] 
			# print data["license"]

			# for row in table:
			# 	print row

		"""

			in_file = csv.reader(in_file, delimiter = t)
			filecontents = [line for line in in_file]


			csv_len = len(list(csv.reader(open(f_in))))
			print csv_len
	 
			# out_file = csv.writer(out_file, quotechar='', quoting=csv.QUOTE_NONE)
			# out_file.writerows(filecontents)

			time_range = collections.Counter()

			for x in filecontents:
				# print x
				
				try:
					month_time = x[3][0:7]
					day_time = x[3][0:10]
					time_range[month_time] +=1
					# print (month_time)

				except:
					output = str(x)
					# f3.write(output)
					pass

			# def sort_csv(line):
			sort_csv = sorted(filecontents, key=lambda row: row[3], reverse=False)
			# print sort_csv

			sort_timerange = sorted(time_range, reverse=False)
			# print time_range

			# for x in sort_csv:
			# 	print x[3]

			cc_ = "CC BY-SA 4.0"
			pd_ = "public domain"
			Pd_ = "Public domain"
			P_ = "Public"
			by_ = "CC BY 4.0"

			for x in sort_timerange:
				
				cc = 0
				pd = 0
				by = 0

				seen = []
				ind = 0

				for a in sort_csv:
					month_ti = a[3][0:7]
					day_ti = a[3][0:10]
					license = a[4]
					# print license
					ind +=1
	
					if (month_ti in seen):
						if (license == cc_):
							cc += 1
						elif (license == by_):
							by += 1
						elif (license == pd_ or license == Pd_ or license == P_):
							pd += 1			
						else:
							print "new: " + license
						
						# if (ind == csv_len):
						output = str(ind) + t + x + t + str(cc) + t + str(pd) + t + str(by)
						print output

					else:
						# print month_ti
						seen.append(month_ti)
					# 	pass

		"""
				# print output







					# # cc = collections.Counter()

					# if (license == cc_):
					# 	cc += 1
					# elif (license == by_):
					# 	by += 1
					# elif (license == pd_ or license == Pd_ or license == P_):
					# 	pd += 1			
					# else:
					# 	print "new: " + license
					
						
					# else:
					# 	print month_ti 
					
					

				

				# print seen
				


				# print seen
					# print cc


					

					# 	if (license == cc_):
					# 		cc += 1
					# 	elif (license == by_):
					# 		by += 1
					# 	elif (license == pd_ or license == Pd_ or license == P_):
					# 		pd += 1			
					# 	else:
					# 		print "new: " + license

						# done.append(month_ti)
						# print a

				
			# output = month_ti + t + str(cc) + t + str(pd) + t + str(by)
			# print output


			# for a in filecontents:
			# 	try:
			# 		month_ti = a[3][0:7]
			# 		day_ti = a[3][0:10]
			# 		license = a[4]
			# 		# print (month_ti,day_ti,license,a,x

			# 		if (month_ti in time_range):
			# 			# print month_ti
			# 			if (license == cc_):
			# 				cc += 1
			# 			elif (license == by_):
			# 				by += 1
			# 			elif (license == pd_ or license == Pd or license == P):
			# 				pd += 1			
			# 			else:
			# 				print "new: " + license
			# 	except:
			# 		pass

			# for x in time_range:
			# 	print x

			# for x in time_range: #time_range: filecontents
			# 	cc = 0
			# 	pd = 0
			# 	by = 0
			# 	cc_ = "CC BY-SA 4.0"
			# 	pd_ = "public domain"
			# 	Pd_ = "Public domain"
			# 	P = "Public"
			# 	by_ = "CC BY 4.0"
				
			# 	for a in filecontents: # filecontents
			# 		try:
			# 			month_ti = a[3][0:7]
			# 			day_ti = a[3][0:10]
			# 			license = a[4]
			# 			# print (month_ti,day_ti,license,a,x)

			# 			seen = []

			# 			if (month_ti == x):
			# 				print month_ti + " uguale"
			# 			else:
			# 				print month_ti

						# 
						# 	# print a
						# 	if (license == cc_):
						# 		cc += 1
						# 	elif (license == by_):
						# 		by += 1
						# 	elif (license == pd_ or license == Pd or license == P):
						# 		pd += 1			
						# 	else:
						# 		output = x + t + license + n
						# 		f3.write(output)
					# except:
					# 	output = a + n
					# 	f3.write(output)
					# 	pass
							

					# f2.write(output + n)
						
					# output = month_ti + t + str(cc) + t + str(pd) + t + str(by)
					# print output
						

					# except:
					# 	output = str(x) + n
					# 	f3.write(output)
					# 	pass

# -----------------------------------
# Launch scripts 

timestamp("data_timestamp") # data_timestamp test


