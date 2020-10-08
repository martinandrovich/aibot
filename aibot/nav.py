#!/usr/bin/env python3

from aibot import hw
from time import sleep
	

def forward(speed = 30):
        # calibrate the gyroscope
        hw.gs.calibrate()
        # drive forward with the color sensor
        hw.forward_light_for(500,"ticks")
        # align with the gyroscope
        hw.motors.turn_degrees(SpeedPercent(5), -hw.gs.angle)
        # drive forward with the gyroscope
        hw.forward_gyro_for(112,"ticks")
        # align with the gyroscope
        hw.motors.turn_degrees(SpeedPercent(5), -hw.gs.angle)

def turn(dir):
    angle = 90 * (-1 if dir == "left" else 1)
    mtank.turn_degrees(SpeedPercent(5),angle)

def drive_square(speed = 30):
    while True:
        forward()
        turn("right")

