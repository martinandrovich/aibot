#!/usr/bin/env python3

from aibot import hw
from time import sleep

from aibot.constants import *

def forward(n = 1):

	# reset the gyroscope
	hw.gs.reset()

	# set speed based on n
	speed = (SPEED_FWD_FAST if n >= INTERSECTIONS_FOR_BOOST else SPEED_FWD)

	# drive forward until (black) intersection noticed; minimum 500 ticks
	# hw.motors.follow_line_until_intersection(DIST_FOLLOW_LINE_MIN, SPEED_FWD)
	hw.motors.follow_line_until_n_intersections(n, DIST_FOLLOW_LINE_MIN, speed)

	# constant forward offset
	# drive forward with the gyroscope at 0 rad
	hw.motors.follow_gyro_for(DIST_INTERSECTION_OFFSET, SPEED_OFFSET, 0)
	
	# align with the gyroscope
	hw.motors.turn_degrees(hw.SpeedPercent(SPEED_TURN), -hw.gs.angle)

def push(n = 1):

	# forward once
	forward(n)
	
	# reset the gyroscope
	hw.gs.reset()

	# drive foward with can until line intersection spotted with front sensor
	hw.motors.follow_line_until_can_intersection(SPEED_PUSH)

	# align with the gyroscope
	hw.motors.turn_degrees(hw.SpeedPercent(SPEED_TURN), -hw.gs.angle)

def back():

	# reset the gyroscope
	hw.gs.reset()

	# drive backwards until intersection with the gyroscope at 0 rad
	hw.motors.follow_gyro_until_intersection(DIST_FOLLOW_LINE_MIN, -SPEED_REV, 0)

	# constant forward offset
	# drive forward with the gyroscope at 0 rad
	hw.motors.follow_gyro_for(DIST_INTERSECTION_OFFSET, SPEED_OFFSET, 0)
	
	# align with the gyroscope
	hw.motors.turn_degrees(hw.SpeedPercent(SPEED_TURN), -hw.gs.angle)

def turn(dir):

	if (dir == "around"):
		angle = 180

	else:
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

	for i in range(n):
		drive(sequence)
		
def test_square(n):

	seq = "f1lf1lf1lf1l"
	drive_repeat(seq, n)
	
def test_push_can(n):

	#  ⬚ ⬚
	#  ⬚ ⊙
	#  ^ ⬚
	#  ⬚ ⬚

	seq = "f2rf1rp1buf1lf1lf3lf1lp1buf1rf1rf1"
	drive_repeat(seq, n)
	
def test_slip(n)

	for i in range(n):
	
		# old method
		forward(n)
		hw.gs.reset()
		hw.motors.follow_line_for_dist(DIST_PUSH_CAN, SPEED_OFFSET)
		hw.motors.turn_degrees(hw.SpeedPercent(SPEED_TURN), -hw.gs.angle)
		
		# wait for input
		input("waiting for input...")
		
		# new method
		forward(n)
		hw.gs.reset()
		hw.motors.follow_line_until_can_intersection(SPEED_PUSH)
		hw.motors.turn_degrees(hw.SpeedPercent(SPEED_TURN), -hw.gs.angle)
		
		# wait for input
		input("waiting for input...")