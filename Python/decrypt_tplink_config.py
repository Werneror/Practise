from pyDes import *

key = b'\x47\x8d\xa5\x0b\xf9\xe3\xd2\xcf'
iv  = '\0\0\0\0\0\0\0\0'
desObject = des(key, ECB, iv, pad=None, padmode=PAD_PKCS5)
data = open('config.bin', 'rb').read()
plain = desObject.decrypt(data)
print(plain)
open('plain.txt', 'wb').write(plain)
