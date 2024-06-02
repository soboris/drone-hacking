from fragproc import Packet

class Bin(object):
	def __init__(self):
		self.bin = []

	def putFragment(self, frag):
		self.bin.append(frag)

	def getFragments(self):
		return self.bin

	def clearBin(self):
		self.bin.clear()

	def checkPacket(self):
		packet = Packet.reassembly(self.getFragments())
		if packet:
			self.clearBin()
		return packet.bytes()
