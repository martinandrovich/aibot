#!/usr/bin/env python3

import time
from time import sleep
from math import pi

from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import GyroSensor

from ev3dev2.motor import Motor
from ev3dev2.motor import MoveTank, follow_for_ms, follow_for_forever
from ev3dev2.motor import SpeedPercent, speed_to_speedvalue, SpeedNativeUnits
from ev3dev2.wheel import EV3Tire

from aibot.constants import *

# ----------------------------------------------------------------------

# sensor objects
cs_l           = ColorSensor(ADDR_CS_L)
cs_r           = ColorSensor(ADDR_CS_R)

gs             = GyroSensor(ADDR_GS)

# motor objects
mot_r          = Motor(ADDR_MOT_R)
mot_l          = Motor(ADDR_MOT_L)
motors         = MoveTank(ADDR_MOT_L, ADDR_MOT_R)

# set object of motors
motors.gyro    = gs
motors.cs_r    = cs_r
motors.cs_l    = cs_l

# ----------------------------------------------------------------------

# extend MoveTank class
# https://stackoverflow.com/questions/972/adding-a-method-to-an-existing-object-instance

def min2(lhs, rhs):
	return (lhs if lhs < rhs else rhs)

def max2(lhs, rhs):
	return (lhs if lhs > rhs else rhs)

def abs2(val):
	# return val * (-1 if val < 0 else 1)
	return val * ((val > 0) - (val < 0))

def saturate(val, limit):
	return max2(min2(val, limit), -limit)

# MoveTank.reset()
def reset(self):

	self.left_motor.reset()
	self.right_motor.reset()

# MoveTank.follow_for_dist()
def follow_for_dist(self, dist, pos_start):

	# callback function, in order to know when to stop line following

	pos_l = abs2(self.left_motor.position  - pos_start["left"])
	pos_r = abs2(self.right_motor.position - pos_start["right"])
	avg   = (pos_l + pos_r) / 2

	return (avg <= dist)

# MoveTank.follow_until_intersection()
def follow_until_intersection(self, min_dist, pos_start, th_black):

	# callback function, in order to know when to stop line following

	pos_l = abs2(self.left_motor.position  - pos_start["left"])
	pos_r = abs2(self.right_motor.position - pos_start["right"])
	avg   = (pos_l + pos_r) / 2

	cs_l  = self.cs_l.reflected_light_intensity
	cs_r  = self.cs_r.reflected_light_intensity

	if (avg < min_dist):
		return True

	else:
		# return ((cs_l > th_black) or (cs_r > th_black))
		return not ((cs_l <= th_black) and (cs_r <= th_black))

def print_cs():

	cs_l  = motors.cs_l.reflected_light_intensity
	cs_r  = motors.cs_r.reflected_light_intensity

	print(cs_l, cs_r)

# MoveTank.follow_until_n_intersections()
def follow_until_n_intersections(self, n, dist_per_intersection, pos_start, th_black):

	# callback function, in order to know when to stop line following

	pos_l = abs2(self.left_motor.position  - pos_start["left"])
	pos_r = abs2(self.right_motor.position - pos_start["right"])
	pos_avg   = (pos_l + pos_r) / 2

	cs_l = self.cs_l.reflected_light_intensity
	cs_r = self.cs_r.reflected_light_intensity

	if (pos_avg < n * dist_per_intersection):
		return True

	else:
		# return ((cs_l > th_black) or (cs_r > th_black))
		return not ((cs_l <= th_black) and (cs_r <= th_black))

# MoveTank.follow_line_dual()
def follow_line_dual(self, kp, ki, kd, speed, sleep_time, follow_for, **kwargs):

	# PID line follower using both color sensors
	# requires defintion of color sensors cs_l and cs_r

	# dt = sleep_time
	# RC = 1 / (2 * pi * LP_CUTOFF_FREQ)

	e = e_prev = i = d_prev = 0.0

	speed = speed_to_speedvalue(speed)
	speed_native_units = speed.to_native_units(self.left_motor)

	# t0 = time.clock()
	# t = 0
	max_speed = SPEED_MAX_NATIVE

	while follow_for(self, **kwargs):

		e = self.cs_l.reflected_light_intensity - self.cs_r.reflected_light_intensity
		i += e

		d = (e - e_prev)
		# d = (e - e_prev) / dt
		# d = d_prev + ((dt / (RC + dt)) * (d - d_prev))
		# d_prev = d

		u = (kp * e) + (ki * i) + (kd * d)
		e_prev = e

		# slewrate
		# if (SLEW_RATE and t < 1):
		# 	t = time.clock() - t0
		# 	max_speed = SPEED_MAX_NATIVE * min(t * SLEW_RATE, 1.0)

		# convert to native speed units (saturated)
		speed_left  = SpeedNativeUnits(saturate(speed_native_units - u, max_speed))
		speed_right = SpeedNativeUnits(saturate(speed_native_units + u, max_speed))

		# if sleep_time:
		# 	sleep(sleep_time)

		self.on(speed_left, speed_right)

	self.stop()

# MoveTank.follow_line_until_intersection()
def follow_line_until_intersection(self, min_dist, speed):

	# follow the line for a specified speed stopping at an
	# intersection after a minimum distance; use dual color sensor

	pos_start = { "left": self.left_motor.position, "right": self.right_motor.position }

	self.follow_line_dual(
		kp           = FOLLOW_LINE_DUAL_P,
		ki           = FOLLOW_LINE_DUAL_I,
		kd           = FOLLOW_LINE_DUAL_D,
		speed        = SpeedPercent(speed),
		sleep_time   = SLEEP_TIME,
		follow_for   = follow_until_intersection,
		min_dist     = min_dist,
		pos_start    = pos_start,
		th_black     = FOLLOW_LINE_DUAL_TH_BLACK
	)

# MoveTank.follow_line_until_n_intersections()
def follow_line_until_n_intersections(self, n, dist_per_intersection, speed):

	# follow the line for a specified speed stopping after
	# n number of intersections; use dual color sensor

	pos_start = { "left": self.left_motor.position, "right": self.right_motor.position }

	self.follow_line_dual(
		kp                    = FOLLOW_LINE_DUAL_P,
		ki                    = FOLLOW_LINE_DUAL_I,
		kd                    = FOLLOW_LINE_DUAL_D,
		speed                 = SpeedPercent(speed),
		sleep_time            = SLEEP_TIME,
		follow_for            = follow_until_n_intersections,
		n                     = n,
		dist_per_intersection = dist_per_intersection,
		pos_start             = pos_start,
		th_black              = FOLLOW_LINE_DUAL_TH_BLACK
	)

# MoveTank.follow_line_for_dist()
def follow_line_for_dist(self, dist, speed):

	# follow the line for a specified distance at a specified speed
	# using dual color sensor

	pos_start = { "left": self.left_motor.position, "right": self.right_motor.position }

	self.follow_line_dual(
		kp           = FOLLOW_LINE_DUAL_P,
		ki           = FOLLOW_LINE_DUAL_I,
		kd           = FOLLOW_LINE_DUAL_D,
		speed        = SpeedPercent(speed),
		sleep_time   = SLEEP_TIME,
		follow_for   = follow_for_dist,
		dist         = dist,
		pos_start    = pos_start
	)

# MoveTank.follow_gyro_for()
def follow_gyro_for(self, dist, speed, angle = 0):

	# follow specified gyro angle at set speed and distance

	pos_start = { "left": motors.left_motor.position, "right": motors.right_motor.position }

	self.follow_gyro_angle(
		kp           = FOLLOW_GYRO_P,
		ki           = FOLLOW_GYRO_I,
		kd           = FOLLOW_GYRO_D,
		speed        = speed,
		target_angle = angle,
		sleep_time   = SLEEP_TIME,
		follow_for   = follow_for_dist,
		dist         = dist,
		pos_start    = pos_start
	)

def follow_gyro_until_intersection(self, min_dist, speed, angle = 0):

	# follow specified gyro angle at set speed until intersection
	# for specified minimum distance

	pos_start = { "left": motors.left_motor.position, "right": motors.right_motor.position }

	self.follow_gyro_angle(
		kp           = FOLLOW_GYRO_P,
		ki           = FOLLOW_GYRO_I,
		kd           = FOLLOW_GYRO_D,
		speed        = speed,
		target_angle = angle,
		sleep_time   = SLEEP_TIME,
		follow_for   = follow_until_intersection,
		min_dist     = min_dist,
		pos_start    = pos_start,
		th_black     = FOLLOW_LINE_DUAL_TH_BLACK
	)

# append extensions
MoveTank.reset = reset

MoveTank.follow_for_dist = follow_for_dist
MoveTank.follow_until_intersection = follow_until_intersection
MoveTank.follow_until_n_intersections = follow_until_n_intersections

MoveTank.follow_line_dual = follow_line_dual
MoveTank.follow_line_until_intersection = follow_line_until_intersection
MoveTank.follow_line_until_n_intersections = follow_line_until_n_intersections
MoveTank.follow_line_for_dist = follow_line_for_dist
MoveTank.follow_gyro_for = follow_gyro_for
MoveTank.follow_gyro_until_intersection = follow_gyro_until_intersection