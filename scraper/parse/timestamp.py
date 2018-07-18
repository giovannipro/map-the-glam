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
			table_sum = data.groupby([timestamp,"license"]).size()

			print table_sum

			for row in table_sum:
				print row

# -----------------------------------
# Launch scripts 

timestamp("data_timestamp") # data_timestamp test


