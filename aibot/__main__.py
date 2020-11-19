#!/usr/bin/env python3

from aibot import app

if __name__ == "__main__":

	try:
		
		app.init()
		app.run()

	except KeyboardInterrupt:
		
		print("\n\nInterrupted via CTRL+C")
		app.exit()
