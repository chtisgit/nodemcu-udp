#!/usr/bin/python3

# This program activates some of the pins on the
# NodeMCU one after another one at a time and
# show status output on the screen

from nodemcu import NodeMcu, NodeMcuError, D, TX, RX
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
		mcu.setOutput(pin)

	while True:
		for i in range(len(PINS)):
			mcu.write(PINS[i], True)
			
			showActivePin(i)
			sleep(SLEEP)
			mcu.write(PINS[i], False)
except NodeMcuError as e:
	print("error:",e)
except KeyboardInterrupt:
	print("\n\nExiting.")

