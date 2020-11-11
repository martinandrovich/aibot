#!/usr/bin/env python3

from aibot import hw
from time import sleep

from aibot.constants import *

def forward(speed = 30):

	# reset the gyroscope
	hw.gs.reset()

	# drive forward with the color sensor
	hw.motors.follow_line_for(DIST_FOLLOW_LINE, speed) # ticks

	# drive forward with the gyroscope (angle = 0)
	hw.motors.follow_gyro_for(DIST_FOLLOW_GYRO, 0, speed)
	
	# align with the gyroscope
	hw.motors.turn_degrees(hw.SpeedPercent(SPEED_TURN), -hw.gs.angle)

def turn(dir):

	angle = 90 * (-1 if dir == "left" else 1)
	hw.motors.turn_degrees(hw.SpeedPercent(SPEED_TURN), angle)

def drive(sequence):
	
	for cmd in sequence:

		action = {
			'f': lambda: turn("left"),
			'p': lambda: turn("right"),
			'w': lambda: forward()
			'l': lambda: forward()
			'r': lambda: forward()
			}[cmd]()

def drive_square(speed = 30):

	while True:
		forward()
		sleep(1)
		turn("right")
		sleep(1)

