#!/usr/bin/python3

# This program activates some of the pins on the
# NodeMCU one after another one at a time and
# show status output on the screen

from nodemcu import NodeMcu, D, TX, RX
from time import sleep
from sys import exit
from common import getIPPort

IPPORT = getIPPort()
SLEEP = 5 # seconds
PINS = D + [RX, TX]
PINNAMES = ["D"+str(i) for i in range(len(D))]+["RX","TX"]

def showActivePin(pin):
	left = " ".join(PINNAMES[:pin])
	mid = PINNAMES[pin]
	right = " ".join(PINNAMES[pin+1:])
	print(" Active PIN: {} *{}* {}          ".format(left, mid, right),end="\r")

try:
	mcu = NodeMcu(IPPORT)
	for pin in PINS:
		err = mcu.setOutput(pin)
		if err != 0:
			print("error: ", mcu.getError(err))
			exit(1)

	while True:
		for i in range(len(PINS)):
			err = mcu.write(PINS[i], True)
			if err != 0:
				print("error: ", mcu.getError(err))
			
			showActivePin(i)
			sleep(SLEEP)
			err = mcu.write(PINS[i], False)
			if err != 0:
				print("error: ", mcu.getError(err))
except KeyboardInterrupt:
	print("\n\nExiting.")

