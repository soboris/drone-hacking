import uos
from ucryptolib import aes

CBC = 2
BLOCK = 16
PAD = b'\x00'

def getKey():
    key = b'vxrl'
    pad = b'='
    return key + pad * (BLOCK * 2 - len(key))

def getIV():
    return uos.urandom(BLOCK)

def encrypt(plaintext, key, iv, mode=CBC):
    cipher = aes(key, mode, iv)
    padded = plaintext + PAD * (BLOCK - len(plaintext) % BLOCK)
    encrypted = cipher.encrypt(padded)
    return encrypted

def decrypt(ciphertext, key, iv, mode=CBC):
    cipher = aes(key, mode, iv)
    decrypted = cipher.decrypt(ciphertext)
    return decrypted
