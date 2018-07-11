#!/usr/bin/python3

from nodemcu import NodeMcu, D
from time import sleep
from sys import exit
from common import getIPPort

mcu = NodeMcu(getIPPort())
err = mcu.setOutput(D[0])
if err != 0:
	print("error: ", mcu.getError(err))
	exit(1)

print("Blinking the LED")
bit = False
while True:
	bit = not bit
	print(" "+("High" if bit else "Low "), end="\r")
	err = mcu.write(D[0], bit)
	if err != 0:
		print("error: ", mcu.getError(err))
		exit(1)
	sleep(.5)
