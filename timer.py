# JOYSTICK CONTROLS
## Press down to start/stop
## Left for 30 seconds
## Right for 90 seconds
## Up/Down hides/unhides the timer

from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
import time
import signal
import sys

# Ctrl-C Handler
def clear_and_exit(sig, frame):
    sense.clear()
    sys.exit(0)
signal.signal(signal.SIGINT, clear_and_exit)

# Sense Config
sense = SenseHat()
sense.set_rotation(180)
sense.low_light = True

# Variables
timer = 90
paused = True
hide = False

# Display Number Function
def displayNum(num):
    pixels = [[0] * 8 for _ in range(8)] # 8x8 array
	
    if num is not None:
        for row in range(8):
            for column in range(4):
                pixels[row][column] = digits[num / 10][row][column] # get the first digit
                pixels[row][column + 4] = digits[num % 10][row][column] # get the second digit
    
    flattened_pixels = reduce(lambda x, y: x + y, pixels)

    for i in range(64):
        if flattened_pixels[i]:
            if num <= 0:
                flattened_pixels[i] = no_time_left
            elif num <= 10:
                flattened_pixels[i] = time_running_out
            elif i % 8 < 4:
                flattened_pixels[i] = first_digit_color
            else:
                flattened_pixels[i] = second_digit_color
        else:
            flattened_pixels[i] = [0, 0, 0] # no color
    
    sense.set_pixels(flattened_pixels)

# Joystick Controls
def pushed_middle(event):
    if event.action == ACTION_PRESSED and timer > 0:
        global paused
        paused = not paused
        
sense.stick.direction_middle = pushed_middle

def resetTimer(time):
    global timer, paused
    timer = time
    paused = True
    displayNum(timer)

def pushed_left(): # since the screen is rotated 180 deg, left is right and right is left
    resetTimer(90)
        
sense.stick.direction_left = pushed_left

def pushed_right():
    resetTimer(30)
        
sense.stick.direction_right = pushed_right

def pushed_up_or_down(event):
    if event.action == ACTION_PRESSED:
        global hide
        if not hide:
            displayNum(None)
        else:
            displayNum(timer)
        hide = not hide
    
sense.stick.direction_up = pushed_up_or_down
sense.stick.direction_down = pushed_up_or_down

# Digit Variables
digits = [
    [ # zero
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0],
    ], [ # one
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 1, 1, 1],
    ], [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 1],
    ], [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [0, 0, 0, 1],
        [1, 1, 1, 0],
        [0, 0, 0, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0],
    ], [
        [1, 0, 1, 0],
        [1, 0, 1, 0],
        [1, 0, 1, 0],
        [1, 0, 1, 0],
        [1, 1, 1, 1],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
    ], [
        [1, 1, 1, 1],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 0],
        [1, 0, 0, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0],
    ], [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 0],
        [1, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0],
    ], [
        [1, 1, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
    ], [
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 0],
    ], [ # nine
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [0, 1, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 1]
    ],
]

# Color Variables
first_digit_color = [255, 0, 255] # purple
second_digit_color = [0, 255, 255] # teal
time_running_out = [255, 140, 0] # dark orange
no_time_left = [255, 0, 0] # red

# Actual Meat of the Code
displayNum(timer)

while True:
    if not paused:
        if (timer == -1):
            displayNum(None)
            timer = 0
        else:
            if not hide:
                displayNum(timer)
            timer -= 1
    time.sleep(1)
