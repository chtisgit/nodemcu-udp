import socket

D = [16, 5, 4, 0, 2, 14, 12, 13, 15]
RX = 3
TX = 1

class NodeMcu:
	def __init__(self, target):
		self.state = [0]*32
		self.Magic = b"LBD!"
		self.Target = target
		self.packId = 0
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.settimeout(1)

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
		
		crc = (~crc) & 0xFFFF
		data = crc
		crc = ((crc << 8) | ((data >> 8) & 0xFF)) & 0xFFFF
		return crc

	def setOutput(self, n):
		i = int(16 + n / 8)
		self.state[i] |= (1 << (n % 8))
		return self.update()

	def setInput(self, n):
		i = int(16 + n / 8)
		self.state[i] &= ~(1 << (n % 8))
		return self.update()

	def write(self, n, val):
		# set port to high if val is true
		i = int(24 + n/8)
		self.state[i] &= ~(1 << (n % 8))
		if val:
			self.state[i] |= (1 << (n % 8))
		return self.update()

	def read(self, n):
		err = self.update()
		if (self.state[int(n/8)] >> (n % 8)) & 1:
			return True, err
		return False, err

	def connected(self):
		package = self.Magic+bytes([0]*(42-len(self.Magic)))
		self.sock.sendto(package, 0, self.Target)
		data, addr = self.sock.recvfrom(32)

		# server will respond with error code 1 (wrong CRC)
		# to message starting with Magic and correct length
		return True if data == 1 else False


	def update(self):
		package = self.Magic
		package += bytes([self.packId & 0xFF, (self.packId >> 8) & 0xFF, (self.packId >> 16) & 0xFF, (self.packId >> 24) & 0xFF])
		package += bytes(self.state)
		#print([hex(x) for x in self.state])
		crc = self.crc(package)
		package += bytes([crc & 0xFF, (crc >> 8) & 0xFF])

		err = -1
		for retries in range(5):
			self.sock.sendto(package, 0, self.Target)
			try:
				data, addr = self.sock.recvfrom(16)
				err = data[0]
				if err == 0 or err == 2:
					for i in range(8):
						self.state[i] = data[i+8]
					return err
			except socket.timeout:
				# receive timed out, retry send and receiv
				pass
			else:
				# some other error
				return -1
		# error after 5 retries
		return err

	def getError(self, code):
		if code == -1:
			return "Internal error. Probably no connection to NodeMCU."
		elif code == 0:
			return "No error"
		elif code == 1:
			return "Wrong CRC"
		elif code == 2:
			return "Invalid setting (output = High for input port)"

