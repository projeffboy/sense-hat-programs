# JOYSTICK CONTROLS
## Press down to turn off/on
## Left/Right to switch modes

from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
import time
import signal
import sys
from enum import Enum

# Ctrl-C Handler
def clear_and_exit(sig, frame):
    sense.clear()
    sys.exit(0)
signal.signal(signal.SIGINT, clear_and_exit)

# Sense Config
sense = SenseHat()
sense.set_rotation(180)
sense.low_light = True

# Mode
class Mode(Enum):
    CLOCK = 0
    TEMP = 1
    HUMIDITY = 2
    OFF = 3

mode = Mode.CLOCK
prev_mode = Mode.OFF

# Joystick Controls
def pushed_middle(event):
    if event.action == ACTION_PRESSED:
        global mode, prev_mode
        if mode == Mode.OFF:
            mode = prev_mode
            prev_mode = Mode.OFF
        else:
            prev_mode = mode
            mode = Mode.OFF
        
sense.stick.direction_middle = pushed_middle

def pushed_left(event): # since the screen is rotated 180 deg, left is right and right is left
    if event.action == ACTION_PRESSED:
        global mode
        mode = Mode((mode.value + 1) % 3)
        
sense.stick.direction_left = pushed_left

def pushed_right(event):
    if event.action == ACTION_PRESSED:
        global mode
        mode = Mode((mode.value - 1) % 3)
        
sense.stick.direction_right = pushed_right

# Clock Variables
digits = [
    [ # zero
        [1, 1, 1],
	    [1, 0, 1],
	    [1, 0, 1],
	    [1, 1, 1]
    ],
    [ # one
    	[0, 1, 0],
    	[1, 1, 0],
    	[0, 1, 0],
    	[1, 1, 1]
    ],
    [
    
	    [1, 1, 1],
	    [0, 1, 1],
	    [1, 1, 0],
	    [1, 1, 1]
    ],
    [
        [1, 1, 1],
        [0, 1, 1],
        [0, 1, 1],
        [1, 1, 1]
    ],
    [
        [1, 0, 1],
        [1, 1, 1],
        [0, 0, 1],
        [0, 0, 1]
    ],
    [
        [1, 1, 1],
        [1, 1, 0],
        [0, 1, 1],
        [1, 1, 1]
    ],
    [
        [1, 0, 0],
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ],
    [
        [1, 1, 1],
        [0, 0, 1],
        [0, 1, 0],
        [1, 0, 0]
    ],
    [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
],
    [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 0, 1]
    ]
]

hour_color = [0, 0, 255] # blue
minute_color = [255, 165, 0] # orange

# Temperature Variables
degree_symbol = [
    [1, 1, 0],
    [1, 1, 0],
    [0, 0, 0],
    [0, 0, 0]
]
C = [
    [1, 1, 1],
    [1, 0, 0],
    [1, 0, 0],
    [1, 1, 1]
]
temp_color = [255, 255, 0] # yellow
temp_sign_color = [255, 0, 0] # red
calibration = 7 # decrease the temperature recorded to offset CPU heat

# Humidity Variables
percent_symbol = [
    [1, 1, 0, 0, 1, 0],
    [1, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1],
    [0, 1, 0, 0, 1, 1]
]
humidity_color = [0, 255, 255] # teal 
percent_color = [255, 0, 255] # purple

# Helper Functions
def flatten(array):
    return reduce(lambda x, y: x + y, array)

def setColorToPx(flattened_pixels, color1, color2):
    for i in range(64):
        if (flattened_pixels[i]):
            if (i < 32):
                flattened_pixels[i] = color1
            else:
                flattened_pixels[i] = color2
        else:
            flattened_pixels[i] = [0, 0, 0] # no color

# Actual Meat of the Code
while True:
    pixels = [[0] * 8 for _ in range(8)] # 8x8 array
    
    if mode == Mode.CLOCK:
        hour = time.localtime().tm_hour
        minute = time.localtime().tm_min

        for row in range(4):
            for column in range(3):
                pixels[row][column + 1] = digits[hour / 10][row][column] # get the first digit
                pixels[row][column + 5] = digits[hour % 10][row][column] # get the second digit
                pixels[row + 4][column + 1] = digits[minute / 10][row][column]
                pixels[row + 4][column + 5] = digits[minute % 10][row][column]
        
        flattened_pixels = flatten(pixels)

        setColorToPx(flattened_pixels, hour_color, minute_color)
        
        sense.set_pixels(flattened_pixels)
        sense.set_pixel(0, 5, 255, 20, 147)
        sense.set_pixel(0, 6, 255, 20, 147)
        time.sleep(1)
    elif mode == Mode.TEMP:
        # get the average of the two temperatures
        temp = int((sense.get_temperature_from_humidity() + sense.get_temperature_from_pressure()) / 2 - calibration)
        
        for row in range(4):
            for column in range(3):
                pixels[row][column + 1] = digits[temp / 10][row][column]
                pixels[row][column + 5] = digits[temp % 10][row][column]
                pixels[row + 4][column + 1] = degree_symbol[row][column]
                pixels[row + 4][column + 5] = C[row][column]
        
        flattened_pixels = flatten(pixels)

        setColorToPx(flattened_pixels, temp_color, temp_sign_color)
        
        sense.set_pixels(flattened_pixels)
        time.sleep(1)
    elif mode == Mode.HUMIDITY:
        humidity = int(sense.get_humidity())
        
        for row in range(4):
            for column in range(3):
                pixels[row][column + 1] = digits[humidity / 10][row][column]
                pixels[row][column + 5] = digits[humidity % 10][row][column]
                
        for row in range(4):
            for column in range(6): 
                pixels[row + 4][column + 2] = percent_symbol[row][column]

        flattened_pixels = flatten(pixels)

        setColorToPx(flattened_pixels, humidity_color, percent_color)

        sense.set_pixels(flattened_pixels)
        time.sleep(1)
    else:
        sense.clear()

sense.clear()
