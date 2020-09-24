#!/usr/bin/env python3

from aibot import hw
from time import sleep
	
def stop():

	hw.stop_motors()

def forward(speed = 50):

	SPEED_FWD_L_FACTOR = 1.0
	SPEED_FWD_R_FACTOR = 1.0

	hw.mot_l.on(speed * SPEED_FWD_L_FACTOR, False)
	hw.mot_r.on(speed * SPEED_FWD_R_FACTOR, False)

	print("waiting for white...")
	while (hw.cs_side.is_black()):
		sleep(0.1)

	sleep(0.8)
	
	print("waiting for black...")
	while (hw.cs_side.is_white()):
		sleep(0.1)

	stop()

def turn(dir):

	valid_dirs = { "left", "right" }
	if dir not in valid_dirs:
		raise ValueError("turn(): dir must be one of %r." % valid_dirs)

	TURN_SPEED_R = 10 # pct
	TURN_SPEED_L = 10 # pct

	speed_l = TURN_SPEED_L * (-1 if dir == "left"  else 1)
	speed_r = TURN_SPEED_R * (-1 if dir == "right" else 1)

	hw.mot_r.on(speed_r, False, False)
	hw.mot_l.on(speed_l, False, False)

	print("waiting for white...")
	while (hw.cs_side.is_black()):
		sleep(0.1)

	sleep(0.8)
	
	print("waiting for black...")
	while (hw.cs_side.is_white()):
		sleep(0.1)

	print("stopping motors...")
	stop()