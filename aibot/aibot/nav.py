#!/usr/bin/env python3

from aibot import hw
from time import sleep

from ev3dev2.sound import Sound

from aibot.constants import *

def forward():

	# reset the gyroscope
	hw.gs.reset()

	# drive forward until (black) intersection noticed; minimum 500 ticks
	# hw.motors.follow_line_until_intersection(DIST_FOLLOW_LINE_MIN, SPEED_FWD)
	hw.motors.follow_line_until_intersection(100, SPEED_FWD)

	# constant forward offset
	# drive forward with the gyroscope at 0 rad
	hw.motors.follow_gyro_for(DIST_FOLLOW_GYRO, SPEED_FWD, 0)
	
	# align with the gyroscope
	hw.motors.turn_degrees(hw.SpeedPercent(SPEED_TURN), -hw.gs.angle)

def back():

	# reset the gyroscope
	hw.gs.reset()

	# drive backwards for push can distance with the gyroscope at 0 rad
	hw.motors.follow_gyro_for(DIST_PUSH_CAN, -SPEED_FWD, 0)

	# align with the gyroscope
	hw.motors.turn_degrees(hw.SpeedPercent(SPEED_TURN), -hw.gs.angle)

def turn(dir):

	angle = 90 * (-1 if dir == "left" else 1)
	hw.motors.turn_degrees(hw.SpeedPercent(SPEED_TURN), angle)

def push():

	# forward once
	forward()
	
	# reset the gyroscope
	hw.gs.reset()

	# drive forward following line for X ticks to push can
	hw.motors.follow_line_for_dist(DIST_PUSH_CAN, SPEED_FWD)

	# reverse using the gyroscope at 0 rad for X ticks
	hw.motors.follow_gyro_for(-DIST_PUSH_CAN, -SPEED_FWD, 0)

	# align with the gyroscope
	hw.motors.turn_degrees(hw.SpeedPercent(SPEED_TURN), -hw.gs.angle)


def uturn():

	# turn around
	turn("left")
	turn("left")

	# drive forward until intersection
	forward()

def drive(sequence):
	
	for cmd in sequence:

		Sound.speak(str(cmd))
		print(cmd)

		action = {
			'f': lambda: forward(),
			'b': lambda: back(),
			'u': lambda: uturn(),
			'p': lambda: push(),
			'l': lambda: turn("left"),
			'r': lambda: turn("right")
			}[cmd]()

def drive_square(speed = 30):

	while True:
		forward()
		sleep(1)
		turn("right")
		sleep(1)
