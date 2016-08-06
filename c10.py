from matasano import *
from base64 import b64decode

file = open('c10.txt', 'r')
ciph = ""
for line in file:
	ciph += line[:-1]
	
ciph = b64decode(ciph)

print(aes_cbc_dec(ciph,"YELLOW SUBMARINE".encode('ascii'),bytes([0]*16)).decode('ascii'))