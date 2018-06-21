#! python
#! /usr/bin python
# Create matrix

import os					# get file path
import csv					# read csv file
import sys					# reset file encoding
import pandas				# work on table and matrix
import numpy				# work on table and matrix

# -----------------------------------
# Utilities

reload(sys)
sys.setdefaultencoding("utf-8")

folder = os.path.dirname(os.path.realpath(__file__))

# -----------------------------------
# Script

file = folder + "/" + "test.tsv"

reader = csv.reader(open(file, "rb"), delimiter="\t")
x = list(reader)
result = numpy.array(x).astype("float")

print(result)

# -----------------------------------
# Launch scripts

