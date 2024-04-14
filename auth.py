import binascii
import uos
import crypto
import hmac

CLA = b'\xff'
INS = {'req':b'\x01','res':b'\x02','sync':b'\x03'}
SHA = 256

counter_size = 4

class Token(object):
    def __init__(self, size=16):
        self.value = uos.urandom(size)

    def getToken(self):
        return self.value

def genToken():
    token = Token()
    return token.getToken()

def authReq():
    return CLA + INS['req'] + genToken()

def authRes(req):
    if bytes([req[0]]) == CLA and bytes([req[1]]) == INS['req']:
        token = req[2:]
        key = crypto.getKey()
        iv = crypto.getIV()
        encrypted = crypto.encrypt(token, key=key, iv=iv)
        return CLA + INS['res'] + iv + encrypted
    return None

def verifyToken(req, res):
    if bytes([res[0]]) == CLA and bytes([res[1]]) == INS['res']:
        token = req[2:]
        key = crypto.getKey()
        iv = res[2:2+crypto.BLOCK]
        encrypted = res[2+crypto.BLOCK:]
        decrypted = crypto.decrypt(encrypted, key, iv).split(b'\x00', 1)[0]
        if decrypted == token:
            return True
    return False

def syncCounter():
    counter = uos.urandom(counter_size)
    key = crypto.getKey()
    iv = crypto.getIV()
    seq = crypto.encrypt(counter, key=key, iv=iv)
    return int.from_bytes(counter, 'big'), CLA + INS['sync'] + iv + seq

def retCounter(sync):
    if bytes([sync[0]]) == CLA and bytes([sync[1]]) == INS['sync']:
        seq = sync[2+crypto.BLOCK:]
        key = crypto.getKey()
        iv = sync[2:2+crypto.BLOCK]
        counter = crypto.decrypt(seq, key, iv).split(b'\x00', 1)[0]
        return int.from_bytes(counter, 'big')
    return None

def hexDigest(msg, counter=None):
    if counter is not None:
        msg = msg + counter.to_bytes(counter_size, 'big')
    digest = hmac.new(crypto.getKey(), msg=msg, digestmod='sha256').hexdigest()
    return digest

def prepPayload(msg, counter=None):
    digest = hexDigest(msg, counter)
    payload = msg + binascii.unhexlify(digest)
    return payload

def chkIntegrity(payload, counter=None):
    msg = payload[0:len(payload)-int(SHA/8)]
    digest = hexDigest(msg, counter)
    if payload[len(msg):] == binascii.unhexlify(digest):
        return True
    return False
