#!/usr/bin/python
# -*- coding: utf-8 -*-

#GIT TEST 2

# The Pins. Use Broadcom numbers.
RED_PIN   = 17
GREEN_PIN = 22
BLUE_PIN  = 24

# Number of color changes per step (more is faster, less is slower).
# You also can use 0.X floats.

###### END ######


import os
import sys
import termios
import tty
import pigpio
import time
from thread import start_new_thread

bright = 255
r = 255.0
g = 0.0
b = 0.0

brightChanged = False
speedChanged = False
abort = False
state = True
flash = False
paused = False
count = 0
flashlevel = 50

steps     = 3


pi = pigpio.pi()

def updateColor(color, step):
	color += step
	
	if color > 255:
		return 255
	if color < 0:
		return 0
		
	return color


def setLights(pin, brightness):
	realBrightness = int(int(brightness) * (float(bright) / 255.0))
	pi.set_PWM_dutycycle(pin, realBrightness)

def getCh():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	
	try:
		tty.setraw(fd)
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		
	return ch

def checkKey():
	global bright
	global brightChanged
	global speedChanged
	global state
	global flash
	global abort
	global paused
	
	while True:
		c = getCh()
		
		if c == '+' and bright < 255 and not brightChanged:
			brightChanged = True
			time.sleep(0.01)
			brightChanged = False
			
			bright = bright + 1
			print ("Current brightness: %d" % bright)
			
		if c == '-' and bright > 0 and not brightChanged:
			brightChanged = True
			time.sleep(0.01)
			brightChanged = False

			
			bright = bright - 1
			print ("Current brightness: %d" % bright)

		if c == '1' and not speedChanged:
			speedChanged = True
			time.sleep(0.01)
			speedChanged = False

			steps = .05
			print steps
			
			print ("Speed Setting 1: Very Slow")

		if c == '2' and not speedChanged:
			speedChanged = True
			time.sleep(0.01)
			speedChanged = False
			
			steps = .1
			print steps
			
			print ("Speed Setting 2: Slow")

		if c == '3' and not speedChanged:
			speedChanged = True
			time.sleep(0.01)
			speedChanged = False
			
			steps = .25
			print steps
			
			print ("Speed Setting 3: Medium")

		if c == '4' and not speedChanged:
			speedChanged = True
			time.sleep(0.01)
			speedChanged = False
			
			steps = 1
			print steps
			
			print ("Speed Setting 4: Slightly Faster Medium")

		if c == '5' and not speedChanged:
			speedChanged = True
			time.sleep(0.01)
			speedChanged = False
			
			steps = 1.5
			print steps
			
			print ("Speed Setting 5: Fast")

		if c == '6' and not speedChanged:
			speedChanged = True
			time.sleep(0.01)
			speedChanged = False
			
			steps = 3
			print steps
			
			print ("Speed Setting 6: Very Fast")

			
		if c == 'p' and state:
			state = False
			time.sleep(0.1)
			print ("Pausing... y")
			
			time.sleep(0.1)
			
			setLights(RED_PIN, 0)
			setLights(GREEN_PIN, 0)
			setLights(BLUE_PIN, 0)

		if c == 's' and state:
                        state = False
                        print ("Stopping on current color...")

                        time.sleep(0.1)

                if c == 'f' and state:
                        flash = True
                        print ("Rave time")

                if c == 'd' and flash:
                        flash = False
                        print ("Back to Normal")
			
		if c == 'r' and not state:
			state = True
			print ("Resuming...")
			
		if c == 'c' and not abort:
			abort = True
			break

start_new_thread(checkKey, ())

print ("+ / - = Increase / Decrease brightness")
print ("p / s / r = Pause Completely / Stop on Color / Resume")
print ("f = flash lights / d to go back to dimming fade")
print ("1 / 2 / 3 / 4 / 5 / 6 for different speeds")
print ("c = Abort Program")



setLights(RED_PIN, r)
setLights(GREEN_PIN, g)
setLights(BLUE_PIN, b)


while abort == False:
        count = count + count
	if state and not brightChanged and not speedChanged and not flash:
		if r == 255 and b == 0 and g < 255:
                        
			g = updateColor(g, steps)
			setLights(GREEN_PIN, g)
		
		elif g == 255 and b == 0 and r > 0:
			r = updateColor(r, -steps)
			setLights(RED_PIN, r)
		
		elif r == 0 and g == 255 and b < 255:
			b = updateColor(b, steps)
			setLights(BLUE_PIN, b)
		
		elif r == 0 and b == 255 and g > 0:
			g = updateColor(g, -steps)
			setLights(GREEN_PIN, g)

		elif g == 0 and b == 255 and r < 255:
			r = updateColor(r, steps)
			setLights(RED_PIN, r)
		
		elif r == 255 and g == 0 and b > 0:
			b = updateColor(b, -steps)
			setLights(BLUE_PIN, b)

	if state and not brightChanged and not speedChanged and flash:
		if r == 255 and b == 0 and g < 255:
                        
			g = updateColor(g, steps)
			if(count % flashlevel == 0):
                                setLights(GREEN_PIN, 0)
   
			setLights(GREEN_PIN, g)
		
		elif g == 255 and b == 0 and r > 0:
			r = updateColor(r, -steps)
			if(count % flashlevel == 0):
                                setLights(RED_PIN, 0)
			setLights(RED_PIN, r)
		
		elif r == 0 and g == 255 and b < 255:
			b = updateColor(b, steps)
			if(count % flashlevel == 0):
                                setLights(BLUE_PIN, 0)
			setLights(BLUE_PIN, b)
		
		elif r == 0 and b == 255 and g > 0:
			g = updateColor(g, -steps)
			if(count % flashlevel == 0):
                                setLights(GREEN_PIN, 0)
			setLights(GREEN_PIN, g)

		elif g == 0 and b == 255 and r < 255:
			r = updateColor(r, steps)
			if(count % flashlevel == 0):
                                setLights(RED_PIN, 0)
			setLights(RED_PIN, r)
		
		elif r == 255 and g == 0 and b > 0:
			b = updateColor(b, -steps)
			if(count % flashlevel == 0):
                                setLights(BLUE_PIN, 0)
			setLights(BLUE_PIN, b)
                
	
print ("Aborting...")

setLights(RED_PIN, 0)
setLights(GREEN_PIN, 0)
setLights(BLUE_PIN, 0)

time.sleep(0.5)

pi.stop()
		


