#!/usr/bin/python3

# In this example the LED on the NodeMCU board can be toggled
# by a button connecting D1 to GND.

from nodemcu import NodeMcu, NodeMcuError, D
from time import sleep
from sys import exit
from common import getIPPort

try:
	mcu = NodeMcu(getIPPort())
	mcu.setOutput(D[0])
	mcu.setInput(D[1])

	print("Press button on D1 to toggle LED")
	bit = False
	changeOk = True

	while True:
		mcu.write(D[0], bit)

		n = mcu.read(D[1])

		# when the button is pressed n == False
		if n == False and changeOk:
			# only toggle the led when the button has been released since the last change
			bit = not bit
			changeOk = False
		elif n == True:
			# when the button is released, allow the user to toggle the LED again
			changeOk = True

except NodeMcuError as e:
	print("error:", e)
