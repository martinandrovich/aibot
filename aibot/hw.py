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

def follow_for_dist (self,dist_ticks) :
	# Callback function, in order to know when to stop. 
	pos_l = self.left_motor.position  - pos_l_start
	pos_r = self.right_motor.position - pos_r_start
	avg   = (pos_l + pos_r) / 2
	return (avg <= dist_ticks)

def follow_line_for(self, dist, speed = 30):	
	# Follow the line with one color sensor on the right
	motors.follow_line(
		kp               = 5.2, 
		ki               = 0.01, 
		kd               = 2.5,
		speed            = speed,
		follow_left_edge = False,
		sleep_time       = 0.001,
		follow_for       = follow_until_dist,
		dist_ticks       = dist
	)
	# stop motors
	self.stop()

def follow_gyro_for(self, dist, angle = 0, speed = 30):
	# Follow the line with the gyro scope 
	motors.follow_gyro_angle(
		kp               = 11.3, 
		ki               = 0.05, 
		kd               = 3.2,
		speed            = speed,
		target_angle     = angle,
		sleep_time       = 0.001,
		follow_for       = follow_until_dist,
    )
	# stop motors
	self.stop()

# append extensions
MoveSteering.stop = stop
MoveSteering.hold = hold
MoveSteering.reset = reset
MoveSteering.drive_straight_for = drive_straight_for
MoveSteering.follow_line_for = follow_line_for
MoveSteering.follow_gyro_for = follow_gyro_for

