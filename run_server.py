#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Nov 10, 2017
Last modified on Nov 16, 2017

@author: Yiting Ju
'''

from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from db.db import DB
from cities import distance_factor, string_similarity_normalized
import time
import uuid
import os

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

def crossdomain(origin=None, methods=None, headers=None,
				max_age=21600, attach_to_all=True,
				automatic_options=True):

	if methods is not None:
		methods = ', '.join(sorted(x.upper() for x in methods))
	if headers is not None and not isinstance(headers, basestring):
		headers = ', '.join(x.upper() for x in headers)
	if not isinstance(origin, basestring):
		origin = ', '.join(origin)
	if isinstance(max_age, timedelta):
		max_age = max_age.total_seconds()

	def get_methods():
		if methods is not None:
			return methods

		options_resp = current_app.make_default_options_response()
		return options_resp.headers['allow']

	def decorator(f):
		def wrapped_function(*args, **kwargs):
			if automatic_options and request.method == 'OPTIONS':
				resp = current_app.make_default_options_response()
			else:
				resp = make_response(f(*args, **kwargs))
			if not attach_to_all and request.method != 'OPTIONS':
				return resp

			h = resp.headers

			h['Access-Control-Allow-Origin'] = origin
			h['Access-Control-Allow-Methods'] = get_methods()
			h['Access-Control-Max-Age'] = str(max_age)
			if headers is not None:
				h['Access-Control-Allow-Headers'] = headers
			return resp

		f.provide_automatic_options = False
		return update_wrapper(wrapped_function, f)
	return decorator

def construct_fuzzy_result(sql_result, query_city_name, query_lat, query_lon):
	for city_record in sql_result:
		lat = city_record["latitude"]
		lon = city_record["longitude"]
		name = city_record["city"]
		if query_lat and query_lon:
			# give distance and string similarity same weight
			city_record["dist"] = distance_factor(query_lat, query_lon, lat, lon)
			city_record["score"] = round(distance_factor(query_lat, query_lon, lat, lon) * 0.5 + \
								string_similarity_normalized(query_city_name, name) * 0.5, 2)
		else:
			city_record["score"] = round(string_similarity_normalized(query_city_name, name), 2)
	if query_lat and query_lon:
		sql_result = sorted(sql_result, 
							key = lambda k: k["dist"],
							reverse = True)
		for city_record in sql_result:
			city_record.pop("dist")
	else:
		pass   # "Results don't need to be sorted in order of relevance/score as shown above."
		sql_result = sorted(sql_result, 
							key = lambda k: k["score"],
							reverse = True)
	return sql_result[:25]


@app.route('/cities')
def search_city_name_fuzzy():
	fuzzy_name = request.args.get("like")
	latitude = request.args.get("latitude")
	longitude = request.args.get("longitude")
	city_db = DB("geonames.db", "city")
	city_db.initialize_db()
	result = city_db.fuzzy_query_for_city_name(fuzzy_name)
	data_response = []
	for record in result:
		temp_response = {}
		temp_response["city"] = record[2]
		temp_response["state"] = record[7]
		temp_response["country"] = record[6]
		temp_response["alternate_names"] = record[3].split(',')
		temp_response["latitude"] = record[4]
		temp_response["longitude"] = record[5]
		data_response.append(temp_response)
	if latitude and longitude and \
			float(latitude) >= -90.0 and float(latitude) <= 90 and \
			float(longitude) >= -180.0 and float(longitude) <= 180:
		data_response = construct_fuzzy_result(data_response, fuzzy_name, float(latitude), float(longitude))
	else:
		data_response = construct_fuzzy_result(data_response, fuzzy_name, None, None)
	return jsonify({
					"header": 
					{
						"module": "DSI",
						"service": "Search_City_Name_fuzzy",
						"created": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
						"organization": "DuPont Pioneer -- JU",
						"request-date": time.strftime("%m/%d/%Y"),
						"transaction-id": str(uuid.uuid1()),
						"vm-instance": "AWS Ubuntu Ju Server 1"
					},
					"data": data_response
				})


@app.route('/cities/<city_name>')
def search_city_name(city_name):
	city_db = DB("geonames.db", "city")
	city_db.initialize_db()
	result = city_db.query_for_city_name(city_name)
	if not result:
		return jsonify({
					"header": 
					{
						"module": "DSI",
						"service": "Search_City_Name",
						"created": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
						"organization": "DuPont Pioneer -- JU",
						"request-date": time.strftime("%m/%d/%Y"),
						"transaction-id": str(uuid.uuid1()),
						"vm-instance": "AWS Ubuntu Ju Server 1"
					},
					"data": {
					}
				}), 204
	city = result[2]
	state = result[7]
	country = result[6]
	lat = result[4]
	lon = result[5]
	alt_names = result[3].split(',')
	return jsonify({
					"header": 
					{
						"module": "DSI",
						"service": "Search_City_Name",
						"created": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
						"organization": "DuPont Pioneer -- JU",
						"request-date": time.strftime("%m/%d/%Y"),
						"transaction-id": str(uuid.uuid1()),
						"vm-instance": "AWS Ubuntu Ju Server 1"
					},
					"data": {
						"city": city,
						"state": state,
						"country": country,
						"alternate_names": alt_names, 
						"latitude": lat,
						"longitude": lon
					}
				})


if __name__ == '__main__':
	app.run(debug = True, host='0.0.0.0', port = 2345, use_reloader=True, threaded=True)


