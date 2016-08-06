from matasano import *
from base64 import b64decode
import pyaes

file = open("c7.txt",'r')
ciph = ""
for line in file:
	ciph += line[:-1]
file.close()

ciph = b64decode(ciph)

key = "YELLOW SUBMARINE".encode('ascii')
print(aes_ecb_dec(ciph,key).decode('ascii'))