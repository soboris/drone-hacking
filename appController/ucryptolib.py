from Crypto.Cipher import AES

class aes(object):
    def __init__(self, key, mode, iv):
        self.cipher = AES.new(key, mode, iv)

    def encrypt(self, plaintext):
        return self.cipher.encrypt(plaintext)

    def decrypt(self, ciphertext):
        return self.cipher.decrypt(ciphertext)
