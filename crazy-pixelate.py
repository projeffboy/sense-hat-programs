from sense_hat import SenseHat
from time import sleep
from random import randint
import signal
import sys

sense = SenseHat()
sense.low_light = False

def clear_and_exit(sig, frame):
    sense.clear()
    sys.exit(0)
signal.signal(signal.SIGINT, clear_and_exit)

while not sense.stick.get_events():
	for x in range(8):
		for y in range(8):
			randColor = (
				randint(0, 255),
				randint(0, 255),
				randint(0, 255),
			)
			sense.set_pixel(x, y, randColor)
	sleep(0.05)

sense.clear()
