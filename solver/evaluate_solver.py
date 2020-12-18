#!/usr/bin/python3

import os
import sys
import re
import subprocess

# define dir of maps based on arguments
dir_maps = os.getcwd() + "/" + sys.argv[1]
bin_file = "build/solver"

# write header to CSV file
out_filename = "solver_stats.csv"
if (os.path.exists(out_filename)):
	os.remove(out_filename)
out_file = open(out_filename, "a")
out_file.write("map, num_cans, time [s]\n")

# iterate all files
for i, filename in enumerate(os.listdir(dir_maps)):

	if (os.path.splitext(filename)[1] != ".txt"):
		continue

	# define full file
	filename_map = sys.argv[1] + "/" + filename
	cmd = "time " + bin_file + " " + filename_map + " > /dev/null"
	print("testing:", filename, "...")

	# run command
	result = subprocess.getoutput(cmd)
	# print("result:", result, "\n")
	
	# check if solution strings exists and parse results
	if (not os.path.exists("solutions/" + filename)):
		print("Solution was not found!\n")
		time = -1
	else:
		time = re.findall('\d*\.?\d+',re.findall("\d*\.?\d+user", result)[0])[0]
		print("time:", time, "s\n")
		
	# extract information from file
	sokoban_map = open(filename_map, "r").read()
	num_cans = sokoban_map.count("J")
	
	# append result to output file
	# map, num_cans, time
	out_file.write(filename + "," + str(num_cans) + "," + str(time) + "\n")
	
out_file.close()
