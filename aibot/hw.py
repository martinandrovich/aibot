#!/usr/bin/env python3

from time import sleep
from statistics import mean

from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import GyroSensor

from ev3dev2.motor import Motor
from ev3dev2.motor import SpeedPercent
from ev3dev2.motor import MoveSteering

from ev3dev2.motor import MoveTank, follow_for_ms, follow_for_forever
from ev3dev2.motor import MoveDifferential
from ev3dev2.wheel import EV3Tire

# ----------------------------------------------------------------------

# constants


ADDR_GS        = "ev3-ports:in1"
ADDR_CS        = "ev3-ports:in2"
STUD_MM        = 8

ADDR_MOT_R     = "ev3-ports:outA"
ADDR_MOT_L     = "ev3-ports:outB"

TH_CS_SIDE     = { "BLACK": 10, "WHITE": 14 } 

# ----------------------------------------------------------------------

# sensor objects
global gs, cs

cs             = ColorSensor(ADDR_CS)
gs             = GyroSensor(ADDR_GS)

# motor objects
global mot_l, mot_r, motors

mot_r          = Motor(ADDR_MOT_R)
mot_l          = Motor(ADDR_MOT_L)
motors         = MoveSteering(ADDR_MOT_L, ADDR_MOT_R)


# ----------------------------------------------------------------------

# extend MoveSteering class
# https://stackoverflow.com/questions/972/adding-a-method-to-an-existing-object-instance

# MoveSteering.stop()
def stop(self):

	self.left_motor.stop_action = "brake"
	self.right_motor.stop_action = "brake"

	self.left_motor.stop()
	self.right_motor.stop()

# MoveSteering.hold()
def hold(self):

	self.left_motor.stop_action = "hold"
	self.right_motor.stop_action = "hold"

	self.left_motor.stop()
	self.right_motor.stop()

# MoveSteering.reset()
def reset(self):

	self.left_motor.reset()
	self.right_motor.reset()

# MoveSteering.drive_straight_for()
def drive_straight_for(self, dist, units, speed_pct = 30):

	valid_units = { "ticks", "cm" }
	if units not in valid_units:
		raise ValueError("drive_straight_for(): units must be one of %r." % valid_units)
	
	# constants
	ENCODER_TICKS_PER_CM = 10
	KP = 10

	# convert distance to encoder ticks
	dist_in_ticks = {
		"ticks": dist,
		"cm":    dist * ENCODER_TICKS_PER_CM
	}

	# calibrate gyro
	print("calibrating gyro...")
	gs.calibrate()
	
	# read current encoder position
	pos_start  = mot_r.position
	pos_des    = pos_start + dist_in_ticks[units]
	
	e = e_prev = i = 0

	dt = 0.01
	kp = 5.2
	ki = 0.01
	kd = 2.5

	# PID loop until desired position reached
	while (mot_r.position <= pos_des):

		e  = gs.angle

		p  = -kp * e
		i += -ki * e * dt
		d  = -kd * (e - e_prev)

		e_prev = e

		dir = p + i + d
		dir = max(min(dir, 100), -100)

		motors.on(dir, SpeedPercent(speed_pct))	
		
	# stop motors
	self.stop()

def turn_for(angle, speed_pct):

	return 0

# append extensions
MoveSteering.stop = stop
MoveSteering.hold = hold
MoveSteering.reset = reset
MoveSteering.drive_straight_for = drive_straight_for

# ----------------------------------------------------------------------

def test():

	mdiff = MoveDifferential(ADDR_MOT_L, ADDR_MOT_R, EV3Tire, 11 * STUD_MM)

	mdiff.on_for_distance(SpeedPercent(30), 300)
	# mdiff.turn_right(SpeedPercent(30), 90)

def test2(dist = 100):

	motors.reset()
	
	mtank = MoveTank(ADDR_MOT_L, ADDR_MOT_R)
	mtank.gyro = gs
	mtank.cs = cs

	mtank.wait_until_not_moving()
	mtank.gyro.calibrate()
	sleep(1)

	# make into a dict
	pos_r_start = mtank.right_motor.position
	pos_l_start = mtank.right_motor.position

	# disable line follow pre intersection
	# gyro_drive for some distance
	# find the line

	def follow_until_dist(self, dist_ticks):

		pos_l = self.left_motor.position  - pos_l_start
		pos_r = self.right_motor.position - pos_r_start
		avg   = (pos_l + pos_r) / 2

		# print("l: ", pos_l, ", r: ", pos_r, ", avg: ", avg)

		return (avg <= dist_ticks)

	# mtank.follow_gyro_angle(
	# 	kp=5.0, ki=0.05, kd=3.2,
	# 	speed=SpeedPercent(20),
	# 	target_angle=0,
	# 	follow_for=follow_until_dist,
	# 	dist_ticks=dist
	# )

	mtank.follow_line(
		kp=5, ki=0.05, kd=0.5,
		speed=SpeedPercent(20),
		follow_left_edge=False,
		sleep_time=0.001,
		follow_for=follow_until_dist,
		dist_ticks=dist
	)

	print("braking...")
	mtank.right_motor.stop_action = "coast"
	mtank.left_motor.stop_action = "coast"
	mtank.right_motor.stop()
	mtank.left_motor.stop()

	sleep(1)

	e = gs.angle
	print("gyro: ", e)

	mtank.right_motor.stop_action = "brake"
	mtank.left_motor.stop_action = "brake"

	mtank.turn_degrees(SpeedPercent(5), -e)

	sleep(1)

# ----------------------------------------------------------------------

# extend ColorSensors class

# ColorSensor.is_black()
def is_black(self):
	return (self.reflected_light_intensity <= TH_CS_SIDE["BLACK"])


# ColorSensor.is_white()
def is_white(self):
	return (self.reflected_light_intensity >= TH_CS_SIDE["WHITE"])

# append extensions
ColorSensor.is_black = is_black
ColorSensor.is_white = is_white

