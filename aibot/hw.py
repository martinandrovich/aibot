#!/usr/bin/env python3

from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import ColorSensor

from ev3dev2.motor import Motor

# constants

ADDR_TS        = "ev3-ports:in3"
ADDR_US        = "ev3-ports:in1"
ADDR_CS_MIDDLE = "ev3-ports:in2"
ADDR_CS_SIDE   = "ev3-ports:in4"

ADDR_MOT_R     = "ev3-ports:outA"
ADDR_MOT_L     = "ev3-ports:outB"

TH_CS_SIDE     = { "BLACK": 10, "WHITE": 14 } 

# sensor objects

ts             = TouchSensor(ADDR_TS)
us             = UltrasonicSensor(ADDR_US)
cs_middle      = ColorSensor(ADDR_CS_MIDDLE)
cs_side        = ColorSensor(ADDR_CS_SIDE)

# motor objects

mot_r          = Motor(ADDR_MOT_R)
mot_l          = Motor(ADDR_MOT_L)

def stop_motors():

	mot_r.stop()
	mot_l.stop()

# extend methods

def is_black(self):
    return (self.reflected_light_intensity <= TH_CS_SIDE["BLACK"])

def is_white(self):
    return (self.reflected_light_intensity >= TH_CS_SIDE["WHITE"])

ColorSensor.is_black = is_black
ColorSensor.is_white = is_white

