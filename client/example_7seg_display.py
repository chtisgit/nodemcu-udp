#!/usr/bin/python3

# This is a more complicated example utilizing a 74HC595 shift register
# to control a 7 segment display. The wiring from the NodeMCU to the 
# shift register is described below. 

from nodemcu import NodeMcu, NodeMcuError, D
from time import sleep
from sys import exit
from common import getIPPort
from time import sleep

# Wiring       Names from the TI data sheet
DS = D[0]    # SER
OE = D[1]    # OE
ST_CP = D[2] # RCLK
SH_CP = D[3] # SRCLK
MR = D[4]    # SRCLR

code = [0xc0,0xf9,0xa4,0xb0,0x99,0x92,0x82,0xf8,0x80,0x90,0xff,0x00]

try:
	mcu = NodeMcu(getIPPort())

	for o in [DS, OE, ST_CP, SH_CP, MR]:
		mcu.setOutput(o)

	mcu.write(OE, False)
	mcu.write(SH_CP, False)
	mcu.write(ST_CP, False)

	num = 0
	while True:
		move = 0x80
		for i in range(0,8):
			mcu.write(DS, code[num] & move != 0)
			mcu.write(SH_CP, False)
			mcu.write(SH_CP, True)
			move >>= 1

		mcu.write(ST_CP, True)
		mcu.write(ST_CP, False)
		mcu.write(SH_CP, False)

		num = (num + 1) % 10
		sleep(2)


except NodeMcuError as e:
	print("error:", e)
