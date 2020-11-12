#!/usr/bin/env python3

from time import sleep

from aibot import hw
from aibot import utils
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

	while True:
		utils.print_all()
		sleep(0.25)

def exit():

	hw.motors.stop()
