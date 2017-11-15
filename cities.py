#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Nov 11, 2017
Last modified on Nov 11, 2017

@author: Yiting Ju
'''

"""
	Normalize distance to a factor btw 0 and 1
	Note: give closer names more weight
"""
def distance_factor(x1, y1, x2, y2):
	dist = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
	if dist < 1:
		return 1
	elif 1 - dist / 90 <= 0:
		return 0
	else:
		return (1 - dist / 90) ** 0.5

"""
	Normalize distance to a factor btw 0 and 1
	Note: give closer places more weight
"""
def string_similarity_normalized(str1, str2):
	return (string_similarity(str1, str2) * 1.0 / (max(len(str1), len(str2)))) ** 0.5

"""
	Calculate the Levenshtein Distance btw two strings
	  ref: https://en.wikipedia.org/wiki/Levenshtein_distance
	note: ignore the case issue
"""
def string_similarity(str1, str2):
	str1 = str1.upper();	
	str2 = str2.upper();
	if len(str1) < len(str2):
		return string_similarity(str2, str1)
	if len(str2) == 0:
		return len(str1)
	previous_row = range(len(str1) + 1)
	row_cnt = 1
	for char2 in str2:
		cur_row = [row_cnt]
		row_cnt += 1
		col_cnt = 0
		for char1 in str1:
			col_cnt += 1
			sub = previous_row[col_cnt - 1]
			if char1 != char2:
				sub += 1
			insert = cur_row[-1] + 1
			delete = previous_row[col_cnt] + 1
			cur_row.append(min(sub, insert, delete))
		previous_row = cur_row
	return previous_row[-1]




if __name__ == "__main__":
	print string_similarity("Saturday", "Sunday")
	print string_similarity_normalized("Saturday", "Sunday")
	print distance_factor(41.85003, -80.65005, 49.03336, -85.8834)

