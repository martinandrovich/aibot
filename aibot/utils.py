#!/usr/bin/env python3

from aibot import hw

# cYkA BlYaT

def print_all():
	
	msg = [ "sensor touch:            " + str(hw.ts.is_pressed), 
	        "sensor ultrasound:       " + str(hw.us.distance_centimeters) + " cm",
	        "sensor color middle:     " + str(hw.cs_middle.reflected_light_intensity),
	        "sensor color side:       " + str(hw.cs_side.reflected_light_intensity),
	        "sensor motor_r position: " + str(hw.mot_r.position),
	        "sensor motor_l position: " + str(hw.mot_l.position)
	      ]

	print("\n".join(msg) + "\n")
