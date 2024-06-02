from fragproc import Packet

class Bin(object):
    def __init__(self):
        self.bin = []

    def putFragment(self, frag):
        for item in self.bin:
            duplicated = True
            for i in range(4):
                if item[i] != frag[i]:
                    duplicated = False
            if duplicated:
                self.bin.remove(item)
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
