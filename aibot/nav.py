#!/usr/bin/env python3

from aibot import hw
from time import sleep

DIST_FOLLOW_LINE = 500
DIST_FOLLOW_GYRO = 80

is_cal = False

def forward(speed = 30):

	# calibrate the gyroscope
	hw.motors.wait_until_not_moving()
	
	global is_cal
	if not is_cal:
		print("calibrating...")
		hw.gs.calibrate()
		is_cal = True

	hw.gs.reset()

	# drive forward with the color sensor
	hw.motors.follow_line_for(DIST_FOLLOW_LINE, speed) # ticks

	# drive forward with the gyroscope (angle = 0)
	hw.motors.follow_gyro_for(DIST_FOLLOW_GYRO, 0, speed)
	
	# align with the gyroscope
	hw.motors.turn_degrees(hw.SpeedPercent(5), -hw.gs.angle)

def turn(dir):

	angle = 90 * (-1 if dir == "left" else 1)
	hw.motors.turn_degrees(hw.SpeedPercent(5), angle)

def drive_square(speed = 30):

	while True:
		forward()
		sleep(1)
		turn("right")
		sleep(1)

