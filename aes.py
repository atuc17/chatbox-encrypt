from Crypto.Cipher import AES
import binascii

def padding(msg):
    res = msg
    l = 16 - len(msg) % 16
    res = res + b'\0'*l
    return res
def encrypt(msg, key):
    assert len(key) == 16
    msg = padding(msg)
    enc = AES.new(key, AES.MODE_CFB, b'This is iv123456')
    message = binascii.hexlify(enc.encrypt(msg))
    return str(message, "ascii")

def decrypt(msg, key):
    assert len(msg) % 16 == 0
    plain = AES.new(key, AES.MODE_CFB, b"This is iv123456")
    plaintext = binascii.unhexlify(bytes(msg, "utf-8"))
    decode_plain = plain.decrypt(plaintext)
    print(decode_plain)
    return str(decode_plain, "ascii")

# ciphertext = encrypt(b'hahahaha', b'this is key12345')
# print(ciphertext)
# print(decrypt(ciphertext, b'this is key12345'))
