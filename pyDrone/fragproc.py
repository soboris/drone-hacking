import math
import binascii

LEN_P = 16

class Packet(object):
    def __init__(self, packet):
        self.cla = bytes([packet[0]])
        self.ins = bytes([packet[1]])
        self.data = packet[2:]

    def frag(self):
        fragments = []
        count = math.ceil(len(self.data)/LEN_P)
        for i in range(0, count):
            header = self.cla + self.ins + bytes([count]) + bytes([i])
            fragments.append(header + self.data[i*LEN_P:(i+1)*LEN_P])
        return fragments

    def bytes(self):
        return self.cla + self.ins + self.data

    @classmethod
    def reassembly(cls, fragments):
        data = b''
        cla = None
        ins = None
        fragments.sort()
        last = fragments[len(fragments)-1]
        if len(fragments) != last[2] or last[2] - last[3] != 1:
            return None
        for fragment in fragments:
            if len(fragments) != fragment[2]:
                break
            if cla and ins:
                if cla != fragment[0] or ins != fragment[1]:
                    raise Exception("ERROR")
            cla = fragment[0]
            ins = fragment[1]
            data += fragment[4:]
        return cls(bytes([cla]) + bytes([ins]) + data)
