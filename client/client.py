#!/usr/bin/python3

from nodemcu import NodeMcu, D
from time import sleep

mcu = NodeMcu(('192.168.1.1', 10000))
err = mcu.setOutput(D[0])
if err != 0:
	print("error code: ", err)

print("Blinking the LED")
bit = False
for i in range(5):
	bit = not bit
	print("High" if bit else "Low")
	err = mcu.write(D[0], bit)
	if err != 0:
		print("error code: ", err)
	sleep(1)