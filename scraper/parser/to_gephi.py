#!/usr/bin/env python
# -*- coding: utf-8 -*- 
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

	file = folder + "/" + my_file + ".tsv"
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
			cat_ = row[4]
		
			if title.strip():
				categories = cat_.split("|")

				for cat in categories:
					final_output = title + t + cat + t + cat + n
					out_file.write(final_output)
					#print(final_output)

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
	
def count_co_occ_6(categories,edges):

	my_input_categories = folder + "/test/" + categories + ".tsv"
	my_input_edges = folder + "/test/" + edges + ".tsv"
	output = folder + "/test/" + categories + "_clean.tsv"

	cat_test = ["a","b","c"]

	cat = [
		"1918 aerial photographs of Switzerland",
		"1919 aerial photographs of Switzerland",
		"1919 photographs of Switzerland",
		"1920 aerial photographs",
		"1920 aerial photographs of Switzerland",
		"1920 photographs of Switzerland",
		"1922 aerial photographs of Switzerland",
		"1923 aerial photographs of Switzerland",
		"1923 photographs",
		"1925 in aviation in Iran",
		"1925 photographs",
		"1928 in Africa",
		"1928 in Madrid",
		"1928 in Tunisia",
		"1929 in aviation in Malta",
		"1930 in Athens",
		"1932 in Alicante",
		"1932 in Barcelona",
		"1932 in Fes",
		"1932 in Oran",
		"1932 in Seville",
		"1932 in Tunis",
		"1932 in Tunisia",
		"1934 in Athens",
		"1967 in aviation in Switzerland",
		"Aadorf",
		"Aarau",
		"Aarburg",
		"Aerial photographs by Walter Mittelholzer",
		"Aerial photographs of aircraft in flight",
		"Aerial photographs of airports in Malta",
		"Aerial photographs of Arbon",
		"Aerial photographs of Athens",
		"Aerial photographs of Cairo",
		"Aerial photographs of Florence",
		"Aerial photographs of Frauenfeld",
		"Aerial photographs of Gibraltar",
		"Aerial photographs of Linz",
		"Aerial photographs of Madrid",
		"Aerial photographs of Piraeus",
		"Aerial photographs of Rome",
		"Aerial photographs of Seville",
		"Aerial photographs of Tehran",
		"Aerial photographs of the Acropolis of Athens",
		"Aerial photographs of the canton of Aargau",
		"Aerial photographs of the canton of Thurgau",
		"Aerial photographs of Tunis",
		"Aerial photographs of Valletta",
		"Aerial photographs of Vesuvius",
		"Aetna",
		"Aleppo",
		"Aleppo in the 1920s",
		"Alkefjellet",
		"Alkhornet",
		"All media needing categories as of 2016",
		"All media needing categories as of 2017",
		"All media supported by Wikimedia CH",
		"Alps of Italy",
		"Altes Schulhaus Horn TG",
		"Altstätten",
		"Amden",
		"Amundsen's Maud Expedition 1918–1925",
		"Arecaceae in Tunisia",
		"Arroyo Abroñigal",
		"Artwork template with implicit creator",
		"Atzmännig",
		"August 1934 photographs",
		"Avenida de Daroca, Madrid",
		"Baghdad in the 1920s",
		"Barbers",
		"Barentsburg",
		"Becchi della Tribolazione",
		"Béchar",
		"Beinwil am See",
		"Béni Abbès",
		"Biskra",
		"Black and white group photographs of men",
		"Black and white photographs by Walter Mittelholzer",
		"Black and white photographs of groups",
		"Black and white photographs of people",
		"Black and white portrait photographs of men",
		"Blida",
		"Boniswil",
		"Borebreen",
		"Bridges in Baghdad",
		"Bridges over the Tigris",
		"Bülach",
		"Bushehr",
		"Cádiz",
		"Calle de Alcalá, Madrid",
		"Calle de Francisco Silvela, Madrid",
		"Calle del Doctor Esquerdo, Madrid",
		"Campo del Moro",
		"Caravans (travel group)",
		"Caravanserais in Iran",
		"Carriages in Tunisia",
		"Cathedral Saint-Vincent-de-Paul of Tunis",
		"CC-PD-Mark",
		"Ceuta",
		"Children with chechias",
		"Chrüzegg (Libingen)",
		"Ciudad Real",
		"Community of Madrid",
		"Connochaetes taurinus of Serengeti National Park",
		"Convair 440 at Zurich International Airport",
		"Convair 440 of Swissair",
		"Corfu town",
		"Coria del Río",
		"D 260 (aircraft)",
		"Dietfurt SG",
		"Dora Baltea",
		"Dussnang",
		"Ebnat-Kappel",
		"Edificio Telefónica, Madrid",
		"El Arenal, Seville",
		"Equus zebra",
		"Eschenbach SG",
		"Esmarkbreen",
		"ETH-BIB Mittelholzer-Abyssinia flight 1934",
		"ETH-BIB Mittelholzer-Inland flights",
		"ETH-BIB Mittelholzer-Kilimanjaro flight 1929-1930",
		"ETH-BIB Mittelholzer-Mediterranean flight 1928",
		"ETH-BIB Mittelholzer-North Africa flight 1932",
		"ETH-BIB Mittelholzer-Persia flight 1924-1925",
		"ETH-BIB Mittelholzer-Spitsbergen flight 1923",
		"ETH-BIB Mittelholzer-Various flights abroad",
		"Evangelische Kirche (Altstätten)",
		"Evangelische Kirche Wängi",
		"Exterior of Cathedral of Seville",
		"Exterior of Palacio de Comunicaciones",
		"Fars Province",
		"Files with no machine-readable author",
		"Fischingen TG",
		"Fishermen",
		"Fishing boats of Norway",
		"Flawil",
		"Flums",
		"Fokker F.VIIb/3m of Swissair",
		"Forlandsundet",
		"Fountains in Tunisia",
		"Frauenfeld",
		"Frick",
		"Fur fashion in 1932",
		"Gallipoli (Italy)",
		"Gates in Qazvin",
		"Gibraltar in the 1920s",
		"Giraffa camelopardalis",
		"Glarus (town)",
		"Gmündertobelbrücke",
		"Gommiswald",
		"Gossau SG",
		"Grabs (St. Gallen, Switzerland)",
		"Gran Paradiso",
		"Granada in 1932",
		"Green Harbor, Norway",
		"Grønfjorden",
		"Guadalquivir",
		"Guadalquivir en Sevilla",
		"GWToolset Batch Upload",
		"Hagia Sophia",
		"Hard",
		"Hermitage of San Isidro, Madrid",
		"Herzogenbuchsee",
		"Hinlopenstretet",
		"Historical building of the Hospital de Santa Cristina",
		"Historical images of Alhambra",
		"Historical images of Athens",
		"Historical images of Bellinzona",
		"Historical images of Cairo Citadel",
		"Historical images of Carrara",
		"Historical images of Chioggia",
		"Historical images of Como",
		"Historical images of Florence",
		"Historical images of Genzano di Roma",
		"Historical images of Giza pyramids",
		"Historical images of Hammerfest",
		"Historical images of Khafra Pyramid",
		"Historical images of Montpellier",
		"Historical images of Mount Etna",
		"Historical images of Ny-Ålesund",
		"Historical images of Pantelleria",
		"Historical images of Rome",
		"Historical images of Saint Peter's Square",
		"Historical images of the Aeolian Islands",
		"Historical images of the Colosseum",
		"Historical images of the Great Sphinx",
		"Historical images of the Vatican City",
		"Historical images of Trajan's Kiosk (Philae)",
		"Historical images of Tromsø",
		"Historical images of Venice",
		"Historical photographs of Arbon",
		"Historical photographs of Frauenfeld",
		"Historical photographs of Konstanz",
		"Historical photographs of the canton of Aargau",
		"Historical photographs of the canton of Thurgau",
		"History of Bandar-e Anzali",
		"History of Etna",
		"Horn TG",
		"Huttwil",
		"Illnau-Effretikon",
		"Images with 10+ annotations",
		"Images with annotations",
		"Independence Square (Tunis)",
		"June 1934 in Greece",
		"Junkers A 20",
		"Junkers F 13 floatplanes",
		"Junkers G.24",
		"Kaiseraugst",
		"Kaltbrunn",
		"Kashan",
		"Katholische Kirche St. Franz Xaver (Horn)",
		"Katholische Kirche St. Remigius (Sirnach)",
		"Kerzers",
		"Kibo (Kilimanjaro)",
		"Kirchberg, Bern",
		"Kirche St. Oswald und Cassian (Sargans)",
		"Kirche von Gommiswald",
		"Kirche von Kaltbrunn",
		"Kloten",
		"Koblenz (AG)",
		"Kollbrunn",
		"Kongsfjorden",
		"Kornhaus (Rorschach)",
		"Krossfjorden",
		"Lake Constance",
		"Lake Hallwil",
		"Lake Lugano",
		"Lake Nemi",
		"Lake of Tunis",
		"Langenthal",
		"Le Locle",
		"Leibstadt",
		"Lenzburg",
		"Leutwil",
		"Levkas",
		"Library symbols",
		"Lilliehöökbreen",
		"Loading (air cargo)",
		"Lockheed Model 9 Orion",
		"Logos associated with education",
		"Male clothing of Tunisia",
		"Malters",
		"Markets in Fes",
		"Markets in Tunis",
		"Martin and Osa Johnson",
		"Mattstogg",
		"Matzingen",
		"Mawenzi peak",
		"Media contributed by the ETH-Bibliothek",
		"Media needing categories as of 1 December 2016",
		"Media needing categories as of 22 December 2016",
		"Media needing categories as of 23 December 2016",
		"Media needing categories as of 25 February 2017",
		"Media needing categories where timestamp category does not exist",
		"Media with locations",
		"Medina of Tetouan",
		"Meersburg",
		"Men at work in Iran",
		"Menziken",
		"Minaret of the Hammouda Pacha Mosque",
		"Minaret of the Youssef Dey Mosque",
		"Minaret of the Zitouna Mosque",
		"Mitra (mountain), Svalbard",
		"Möhlin",
		"Monacofjellet",
		"Mosques in Baghdad",
		"Mosques in Iraq",
		"Mosques in Isfahan",
		"Mount Olympus",
		"Mountains of Iran",
		"Mountains of Svalbard",
		"Neftenbach",
		"New Julfa",
		"Newtontoppen",
		"Nile Delta",
		"Oberburg",
		"Oberentfelden",
		"Oberfrick",
		"Oberwangen",
		"Olten",
		"Oran in 1932",
		"Oscar II Land",
		"Otto Wagner",
		"Pages with map",
		"Pages with maps",
		"Parque del Buen Retiro",
		"Paseo de la Emita del Santo, Madrid",
		"Paseo de Recoletos",
		"Payerne",
		"PD ineligible",
		"PD Old",
		"PD-1996",
		"PD-old-75",
		"People of Biskra",
		"Pfäffikon ZH",
		"Pfeffikon",
		"Pfynwald",
		"Philopappos Hill",
		"Photographs by Swissair",
		"Piraeus in the 1930s",
		"Piz Medel",
		"Piz Scopi",
		"Plaza de Cibeles, Madrid",
		"Plaza de la Armería, Madrid",
		"Plaza de Oriente, Madrid",
		"Plaza de toros de la Fuente del Berro",
		"Plaza de toros de las Ventas",
		"Plaza Mayor, Madrid",
		"Pratteln",
		"Prins Karls Forland",
		"Puerta de Alcalá, Madrid",
		"R-RECI (aircraft)",
		"RAF Hal Far",
		"Ramses II colossal granite statue in Memphis",
		"Raudfjorden",
		"Regensberg ZH",
		"Reinach AG",
		"Romont",
		"Roof terraces in Tunisia",
		"Rorschach",
		"Royal Palace of Madrid",
		"Rypefjord, Hammerfest",
		"Rypefjorden",
		"Sailboats",
		"SAIS-Werke Horn TG",
		"Salamis",
		"Salgesch",
		"Salzburg Airport",
		"San Isidro Cemetery, Madrid",
		"San Justo Cemetery, Madrid",
		"Santa Cruz, Seville",
		"Sargans",
		"Sarmenstorf",
		"Schloss Arbon",
		"Schloss Brestenberg",
		"Schloss Hallwyl",
		"Schloss Sargans",
		"Schloss Werdenberg",
		"Schnebelhorn",
		"Schwellbrunn",
		"Seaplane stations",
		"Seengen",
		"Serengeti",
		"Sète",
		"Seville in the 1920s",
		"Sirnach",
		"Sitting people",
		"Smyrna",
		"Solothurn",
		"Souk El Bechmak",
		"Souqs in Tunis",
		"Sphinx of Memphis",
		"St. Martin, Arbon",
		"St. Nikolaus (Altstätten)",
		"Stadtkirche Glarus",
		"Steinhof, Vienna",
		"Streets in the medina of Tunis",
		"Stromboli",
		"Suhr AG",
		"Sveabreen",
		"Swissair aircraft at Zurich International Airport",
		"Teatro Real, Madrid",
		"Tehran",
		"Tehran in the 1920s",
		"Tempelfjorden",
		"Temple of Ptah in Memphi",
		"Tetouan",
		"Timgad",
		"Tödi",
		"Torre del Oro",
		"Tre Kroner",
		"Turbenthal",
		"Türmlihuus",
		"Untersberg",
		"Uzwil",
		"Vesuvius in 1924",
		"Vesuvius in 1928",
		"Vesuvius in 1932",
		"Vesuvius in 1934",
		"Views of Algeciras",
		"Views of Baghdad",
		"Views of Bou Kornine",
		"Views of Isfahan",
		"Views of Lycabettus",
		"Views of the medina of Tunis",
		"Villa Olmo (Como)",
		"Volketswil",
		"Walter Mittelholzer",
		"Wängi",
		"Werdenberg",
		"Wettingen",
		"Wiesendangen",
		"Wijdefjorden",
		"Wooden boats",
		"Woodfjorden",
		"Ymerbukta",
		"Zayandeh Rud",
		"Zug"
		]

	try:
		with open(my_input_categories, "rb") as in_ca_file, \
			open(my_input_edges, "rb") as in_ed_file, \
			open(output, 'wb') as out_file:

			in_ca_file = csv.reader(in_ca_file, delimiter = t)
			filecontents_ca = [line for line in in_ca_file]

			in_ed_file = csv.reader(in_ed_file, delimiter = t)
			filecontents_ed = [line for line in in_ed_file]

			for c in cat:
				index = 0
				#print(c)

				for x in filecontents_ed:
					index += 1
					title = x[0]
					categories = x[1]
					output_a = title + t + categories
					#print(categories)

					if title.strip():
						cate = categories.split("|")

					for cat_1 in cate:
						count = 0
						#print(cat_1)

						if c in cate and c != cat_1:
							count += 1

						if c != cat_1 and count != 0:
							output_b = str(index) + t + c + "_" + cat_1 + t + c + t + cat_1 + t + str(count)
							output_b_ = output_b + n

							print (index)
							out_file.write(output_b_)

	
	except IOError as e:
		print 'Operation failed: %s' % e.strerror


# -----------------------------------
# Launch scripts

edges("test/test_cat")

# edges("to_gephi_test") # to_gephi_test eth-biblioteck-uploads2016
# nodes("20170419_Media_contributed_by_the_ETH-Bibliothek-info")

# count_co_occ_6("categories","test")


