#! python
#! /usr/bin python
# Extract data from json

import os					# get file path
import urllib, json, io		# read json
from urllib import urlopen	# open file
import sys					# reset file encoding

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

# -----------------------------------
# Launch scripts 

extract()
