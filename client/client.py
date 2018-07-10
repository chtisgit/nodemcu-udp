#!/usr/bin/python3

import socket
import crcmod

class NodeMcu:
	def __init__(self, target):
		self.state = [0]*32
		self.Magic = b"LBD!"
		self.Target = target
		self.packId = 0
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def crc(self, data):
		crc = 0xFFFF;
		if len(data) == 0:
			return ~crc

		p = 0	
		while p < len(data):
			d = 0xFF & data[p]
			for i in range(8):
				if((crc & 1) ^ (d & 1)):
					crc = (crc >> 1) ^ 0x8408
				else:
					crc >>= 1
				d >>= 1
			p += 1
		
		crc = ~crc
		data = crc
		crc = (crc << 8) | ((data >> 8) & 0xFF)
		return crc

	def setOutput(self, n):
		i = int(16 + n / 8)
		self.state[i] |= (1 << (n % 8))
		return self.update()

	def setInput(self, n):
		i = int(16 + n / 8)
		self.state[i] &= ~(1 << (n % 8))
		return self.update()

	def output(self, n, val):
		i = int(24 + n/8)
		self.state[i] &= ~(1 << (n % 8))
		bit = 1 if val else 0
		self.state[i] |= (bit << (n % 8))
		return self.update()

	def input(self, n):
		err = self.update()
		if (self.state[int(n/8)] >> (n % 8)) & 1:
			return True, err
		return False, err

	def update(self):
		package = self.Magic
		package += bytes([self.packId & 0xFF, (self.packId >> 8) & 0xFF, (self.packId >> 16) & 0xFF, (self.packId >> 24) & 0xFF])
		package += bytes(self.state)
		crc = self.crc(package)
		package += bytes([crc & 0xFF, (crc >> 8) & 0xFF])
		print(package)
		self.sock.sendto(package, 0, self.Target)
		data, addr = self.sock.recvfrom(32)
		return data[0] # error code


mcu = NodeMcu(('192.168.1.1', 10000))
mcu.setOutput(1)
print("error code: ")
print(mcu.output(1, True))
