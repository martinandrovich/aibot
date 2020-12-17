#!/usr/bin/python3

import os
import sys
import re

# define bared based on arguments
dir_input = os.getcwd() + "/" + sys.argv[1]
dir_output = os.getcwd() + "/txt"

# create output directory
os.makedirs(dir_output, exist_ok=True)

# iterate all files
for i, filename in enumerate(os.listdir(dir_input)):
	
	# load sokoban map from file
	file = open(dir_input + "/" + filename, "r")
	lines = file.readlines()
	
	# filter out whitespaces chars
	# lines = [x.replace('\n', '') for x in lines]
	lines = list(filter(lambda x: not re.match(r'^\s*$', x), lines))
	
	# find index of last line containing a hashtag
	index_of_last_hashtag = [idx for idx, s in enumerate(lines) if "##" in s][-1]

	# remove all lines after the last hashtag
	lines = lines[0:index_of_last_hashtag + 1]
	
	# convert list to string
	text = ''.join(lines)
	
	# ignore if contains "*" (can on goal)
	if "*" in text:
		continue
	
	# replace characters
	text = text.replace(".", "G").replace("#", "X").replace("$", "J").replace("@", "M").replace("*", "?").replace(" ", ".").rstrip("\n")
	
	# print
	# print("file: ", dir + "/" + filename)
	# print("index_of_last_hashtag: ", index_of_last_hashtag)
	# print(text)
	
	# output to file
	n = int(''.join(filter(str.isdigit, os.path.splitext(filename)[0])))
	# print(text,  file=open(dir_output + "/" + os.path.splitext(filename)[0] + ".txt", "w"))
	print(text,  file=open(dir_output + "/map" + str(n) + ".txt", "w"))