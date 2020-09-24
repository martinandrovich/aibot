#!/usr/bin/env python3

from time import sleep

from aibot import hw
from aibot import utils
from aibot import nav

def init():

	hw.reset_motors()
	hw.reset_encoders()

def run():

	print("ev3 aibot\n")

	while True:

		utils.print_all()
		# nav.drive_straight()
		sleep(0.5)

def exit():

	hw.stop_motors()
