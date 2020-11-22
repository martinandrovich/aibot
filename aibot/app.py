#!/usr/bin/env python3

from time import sleep

from aibot import hw
from aibot import nav

def init():

	print("initializing aibot...")
	
	# halt and reset motors
	hw.motors.stop()
	hw.motors.reset()
	
	sleep(1)

	# calibrate gyroscope
	hw.motors.wait_until_not_moving()
	hw.gs.calibrate()

	print("aibot has been initialized")

def run():

	# filename = input("Path to file: ")
	filename = "solutions/map1.txt"

	file = open(filename)
	seq = file.read().replace("\n", " ")
	file.close()

	print("executing: ", seq)
	sleep(1)

	nav.drive(seq)

def exit():

	hw.motors.stop()
