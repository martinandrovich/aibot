#!/usr/bin/env python3

from aibot import hw
from time import sleep

from aibot.constants import *

def forward(n = 1):

	# reset the gyroscope
	hw.gs.reset()

	# drive forward until (black) intersection noticed; minimum 500 ticks
	# hw.motors.follow_line_until_intersection(DIST_FOLLOW_LINE_MIN, SPEED_FWD)
	hw.motors.follow_line_until_n_intersections(n, DIST_BETWEEN_INTERSECTION, SPEED_FWD)

	# constant forward offset
	# drive forward with the gyroscope at 0 rad
	hw.motors.follow_gyro_for(DIST_FOLLOW_GYRO, SPEED_FWD, 0)
	
	# align with the gyroscope
	hw.motors.turn_degrees(hw.SpeedPercent(SPEED_TURN), -hw.gs.angle)

def push(n = 1):

	# forward once
	forward(n)
	
	# reset the gyroscope
	hw.gs.reset()

	# drive forward following line for X ticks to push can
	hw.motors.follow_line_for_dist(DIST_PUSH_CAN, SPEED_FWD)

	# align with the gyroscope
	# hw.motors.turn_degrees(hw.SpeedPercent(SPEED_TURN), -hw.gs.angle)

def back():

	# reset the gyroscope
	hw.gs.reset()

	# drive backwards for push can distance with the gyroscope at 0 rad
	# hw.motors.follow_gyro_for(DIST_PUSH_CAN, -SPEED_FWD, 0)
	hw.motors.follow_gyro_until_intersection(100, -SPEED_FWD, 0)
	

	# align with the gyroscope
	hw.motors.turn_degrees(hw.SpeedPercent(SPEED_TURN), -hw.gs.angle)

def turn(dir):

	if (dir == "around"):
		angle = 180

	else
		angle = 90 * (-1 if dir == "left" else 1)
	
	hw.motors.turn_degrees(hw.SpeedPercent(SPEED_TURN), angle)

def drive(sequence):

	for i, cmd in enumerate(sequence):

		if cmd.isnumeric():
			continue

		if cmd in ["f", "p"]:
			n = int(sequence[i+1])

		actions = {
			'f': lambda: forward(n),
			'p': lambda: push(n),
			'b': lambda: back(),
			'u': lambda: turn("around"),
			'l': lambda: turn("left"),
			'r': lambda: turn("right")
		}[cmd]()

def drive_repeat(sequence, n):

	# square test:
	# f1 l f1 l f1 l f1 l
	
	# push can test:
	# f2 l f1 l p1b u f1 r f1 r f3 r f1 r p1b u f1 l f1 l f1

	#  ⬚⬚
	#  ⬚⊙
	#  ⧋⬚
	#  ⬚⬚

	for i in range(n):
		drive(sequence)