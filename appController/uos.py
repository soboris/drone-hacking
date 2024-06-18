from Crypto import Random

def urandom(block):
    return Random.new().read(block)
