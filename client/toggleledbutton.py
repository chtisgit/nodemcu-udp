#!/usr/bin/python3

# In this example the LED on the NodeMCU board can be toggled
# by a button connecting D1 to GND.

from nodemcu import NodeMcu, D
from time import sleep
from sys import exit
from common import getIPPort

mcu = NodeMcu(getIPPort())
err = mcu.setOutput(D[0])
if err != 0:
	print("error: ", mcu.getError(err))
	exit(1)

err = mcu.setInput(D[1])
if err != 0:
	print("error: ", mcu.getError(err))
	exit(1)

print("Press button on D1 to toggle LED")
bit = False
changeOk = True

while True:
	err = mcu.write(D[0], bit)
	if err != 0:
		print("error: ", mcu.getError(err))
		exit(1)

	n, err = mcu.read(D[1])

	# when the button is pressed n == False
	if err == 0 and n == False and changeOk:
		# only toggle the led when the button has been released since the last change
		bit = not bit
		changeOk = False
	elif err == 0 and n == True:
		# when the button is released, allow the user to toggle the LED again
		changeOk = True

