#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Nov 10, 2017
Last modified on Nov 10, 2017

@author: Yiting Ju
'''

import csv
import os
import sqlite3
import sys


"""
	Employ a sqlite database to host data
"""
reload(sys)  
sys.setdefaultencoding('utf8')

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

"""
	Class DB to handle database related operations
"""
class DB:
	def __init__(self, db_name, table_name):
		self.db = db_name
		self.table = table_name

	"""
		Create the database/table and load the data into it
	"""
	def initialize_db(self):
		self.create_table()
		data_file_path = os.path.join(DIR_PATH, "data", "canada_usa_cities.tsv")
		self.load_tsv_and_insert(data_file_path)

	def create_table(self):
		conn = sqlite3.connect(self.db)
		cursor = conn.cursor()
		# Create the table to host geonames city data
		#   seems like the raw data is messy
		cursor.execute("""DROP TABLE IF EXISTS """ + self.table + """;""")
		cursor.execute("""CREATE TABLE """ + self.table + """
					(id integer, name text, ascii text, alt_name text, lat real, long real, country text, state text);
					""")
		conn.commit()
		conn.close()

	def load_tsv_and_insert(self, tsv_file_path):
		conn = sqlite3.connect(self.db)
		cursor = conn.cursor()
		with open(tsv_file_path) as tsvfile:
			reader = csv.reader(tsvfile, delimiter = '\t')
			first_line = True
			for line in reader:
				if first_line:
					first_line = False
					continue
				query = """INSERT INTO """ + self.table + """ (id, name, ascii, alt_name, lat, long, country, state) VALUES ({}, "{}", "{}", "{}", {}, {}, "{}", "{}");""".format( \
							int(line[0]), line[1], line[2], line[3], float(line[4]), float(line[5]), line[8], line[10])
				# print query
				cursor.execute(query)
				# for cell in line:
				# 	print cell.encode("utf8")
		conn.commit()
		conn.close()
	
	def query_for_city_name(self, city_name):
		conn = sqlite3.connect(self.db)
		cursor = conn.cursor()
		query = """SELECT * FROM """ + self.table + \
				""" WHERE name = '""" + city_name + """';"""
		cursor.execute(query)		
		results = []
		fetchRes = cursor.fetchall()
		if not fetchRes:
			return []
		for record in fetchRes[0]:
			results.append(record)
		return results

	def fuzzy_query_for_city_name(self, fuzzy_city_name):
		conn = sqlite3.connect(self.db)
		cursor = conn.cursor()
		query = """SELECT * FROM """ + self.table + \
				""" WHERE name LIKE '%""" + fuzzy_city_name + """%'
				;"""
		cursor.execute(query)		
		results = []
		for records in cursor.fetchall():
			temp_res = []
			for record in records:
				temp_res.append(record)
			results.append(temp_res)
		return results


if __name__ == "__main__":
	city_db = DB("geonames.db", "city")
	city_db.create_table()
	data_file_path = os.path.join(DIR_PATH, "data", "canada_usa_cities.tsv")
	city_db.load_tsv_and_insert(data_file_path)
	city_db.query_for_city_name("Des Moines")
