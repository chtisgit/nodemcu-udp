#!/usr/bin/python3

from nodemcu import NodeMcu, NodeMcuError, D
from time import sleep
from sys import exit
from common import getIPPort

try:
	mcu = NodeMcu(getIPPort())
	mcu.setOutput(D[0])

	print("Blinking the LED")
	bit = False
	while True:
		bit = not bit
		print(" "+("High" if bit else "Low "), end="\r")
		mcu.write(D[0], bit)
		sleep(.5)
except NodeMcuError as e:
	print("error:", e)
