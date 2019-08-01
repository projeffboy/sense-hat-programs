from sense_hat import SenseHat
from time import sleep
from random import randint
import signal
import sys

sense = SenseHat()

def clear_and_exit(sig, frame):
    sense.clear()
    sys.exit(0)
signal.signal(signal.SIGINT, clear_and_exit)

while not sense.stick.get_events():
	randColor = (
		randint(0, 255),
		randint(0, 255),
        randint(0, 255),
	)
	x = randint(0, 7)
	y = randint(0, 7)
	
	sense.set_pixel(x, y, randColor)
	sleep(1)

sense.clear()
