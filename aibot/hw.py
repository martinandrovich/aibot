#!/usr/bin/env python3

from time import sleep
from statistics import mean

from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import GyroSensor

from ev3dev2.motor import Motor
from ev3dev2.motor import SpeedPercent, speed_to_speedvalue, SpeedNativeUnits
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

# ----------------------------------------------------------------------

# sensor objects
global gs, cs

cs             = ColorSensor(ADDR_CS)

cs_l           = ColorSensor(ADDR_CS)
cs_r           = ColorSensor("ev3-ports:in3")

gs             = GyroSensor(ADDR_GS)

# motor objects
global mot_l, mot_r, motors

mot_r          = Motor(ADDR_MOT_R)
mot_l          = Motor(ADDR_MOT_L)
motors         = MoveTank(ADDR_MOT_L, ADDR_MOT_R)

# set object of motors
motors.gyro    = gs
motors.cs      = cs
motors.cs_r    = cs_r
motors.cs_l    = cs_l

# ----------------------------------------------------------------------

# extend MoveSteering class
# https://stackoverflow.com/questions/972/adding-a-method-to-an-existing-object-instance

# MoveSteering.reset()
def reset(self):

	self.left_motor.reset()
	self.right_motor.reset()

# MoveSteering.follow_for_dist()
def follow_for_dist(self, dist, pos_start):
	
	# callback function, in order to know when to stop

	pos_l = self.left_motor.position  - pos_start["left"]
	pos_r = self.right_motor.position - pos_start["right"]
	avg   = (pos_l + pos_r) / 2

	return (avg <= dist)

# MoveSteering.follow_until_intersection()
def follow_until_intersection(self, min_dist, pos_start, th_black = 7):
	
	# callback function, in order to know when to stop

	pos_l = self.left_motor.position  - pos_start["left"]
	pos_r = self.right_motor.position - pos_start["right"]
	pos_avg   = (pos_l + pos_r) / 2

	cs_l = self.cs_l.reflected_light_intensity
	cs_r = self.cs_r.reflected_light_intensity

	if (pos_avg < min_dist):
		return True

	else:
		# return ((cs_l > th_black) or (cs_r > th_black))
		return not ((cs_l <= th_black) and (cs_r <= th_black))

# MoveSteering.follow_line_for()
def follow_line_for(self, dist, speed = 30):

	# follow the line with one color sensor on the right

	pos_start = { "left": self.left_motor.position, "right": self.right_motor.position }

	self.follow_line_dual(
		kp               = 3.2, 
		ki               = 0.01, 
		kd               = 2.0,
		speed            = SpeedPercent(speed),
		#follow_left_edge = False,
		sleep_time       = None,
		follow_for       = follow_until_intersection,
		# follow_for       = follow_for_dist,
		min_dist         = dist,
		pos_start        = pos_start,
		th_black         = 45
	)

	# stop motors
	# self.stop()

# MoveSteering.follow_gyro_for()
def follow_gyro_for(self, dist, angle = 0, speed = 30):
	
	# follow the line with the gyro scope

	pos_start = { "left": motors.left_motor.position, "right": motors.right_motor.position }
	
	motors.follow_gyro_angle(
		kp               = 3.0, 
		ki               = 0.01, 
		kd               = 2.0,
		speed            = speed,
		target_angle     = angle,
		sleep_time       = None,
		follow_for       = follow_for_dist,
		dist             = dist,
		pos_start        = pos_start
	)

	# stop motors
	# self.stop()

def follow_line_dual(self, kp, ki, kd, speed, sleep_time, follow_for, **kwargs):
	
	e = e_prev = i = 0.0

	speed = speed_to_speedvalue(speed)
	speed_native_units = speed.to_native_units(self.left_motor)
	
	while follow_for(self, **kwargs ):

		e = self.cs_l.reflected_light_intensity - self.cs_r.reflected_light_intensity
		i += e
		d = (e - e_prev)
		u = (kp * e) + (ki * i) + (kd * d) 
		e_prev = e
		
		speed_left  = SpeedNativeUnits(speed_native_units - u)
		speed_right = SpeedNativeUnits(speed_native_units + u)
		
		if sleep_time:
			sleep(sleep_time)
		
		self.on(speed_left, speed_right)

	self.stop()

# append extensions
MoveTank.reset = reset
MoveTank.follow_line_for = follow_line_for
MoveTank.follow_gyro_for = follow_gyro_for
MoveTank.follow_line_dual = follow_line_dual

