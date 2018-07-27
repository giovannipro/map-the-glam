#! python
#! /usr/bin python
# Extract data from json

import os					# get file path
import urllib, json, io		# read json
from urllib import urlopen	# open file
import sys					# reset file encoding
import string
import csv

reload(sys)
sys.setdefaultencoding("utf-8")

# -----------------------------------
# Utilities

folder = os.path.dirname(os.path.realpath(__file__))
t = "\t"

# -----------------------------------
# Main variables

my_file = "test"

file = folder + "/" + my_file + ".json"
output = folder + "/" + my_file + "_clean.tsv"

# -----------------------------------
# scripts 

def extract():

	response = urlopen(file).read()
	data = json.loads(response)
	#print data

	with open(output, "w") as f:
		#json.dump(data, f)
		#f.write(data)
		#f.write("test")

		for x in data["query"]["allimages"]:
			try:
				tit = x["name"]
				tim = x["timestamp"]
				cat = x["extmetadata"]["Categories"]["value"]
				#des = x["extmetadata"]["ImageDescription"]["value"]
				lic = x["extmetadata"]["LicenseShortName"]["value"]

				if (tit != ""):
					f.write(tit + t)
				else:
					f.write("-" + t)

				if (tit != ""):
					f.write(tim + t)
				else:
					f.write("-" + t)

				if (cat != ""):
					f.write(cat + t)
				else:
					f.write("-" + t)
					#print cat 

				if (lic != ""):
					f.write(lic)
				else:
					f.write("-")

				f.write("\n")

			except IOError:
				print('An error occured trying to read the file.')
				continue

			except ImportError:
				print "NO module found"
				continue
				
			except EOFError:
				print('Why did you do an EOF on me?')
				continue

			except KeyboardInterrupt:
				print('You cancelled the operation.')
				continue

			except:
				#print('An error occured.')
				print (tit + "\t" + tim + "\t" + cat + "\t" + lic)
				continue

#!/usr/bin/python
"""
Read TSV from stdin and output as JSON.
"""

def tsv_to_json(f_name):

	func = "tsv_to_json"
	index = 0

	f_in = folder + "/data/" + f_name + ".tsv"
	f_out = folder + "/data/" + f_name + "_" + func + "-output.tsv" 

	with open(f_in, "r") as f1:
		with open(f_out, "w") as f2:

			tsv_file = csv.reader(f1, delimiter=t)

			for file in tsv_file:
				if (index==0):
					a = file[1]
					b = file[2]
					c = file[3]
					d = file[4]

			for file in tsv_file:
				if (index==0):

				print file

	
# -----------------------------------
# Launch scripts 

extract()
# tsv_to_json("test")

