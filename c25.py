from matasano import *
from base64 import b64decode
import struct

file = open('c25.txt','r')
plain = ""
for line in file:
	plain += line[:-1]
file.close()

plain = b64decode(plain)
plain = aes_ecb_dec(plain,"YELLOW SUBMARINE".encode('ascii'))
plain = pkcs7_unpad(plain)

key = randbytes(16)
nonce = randbytes(8)
ciph = aes_ctr(plain,key,nonce)

def edit(offset,plaintext):
	global key,nonce,ciph
	new_block = aes_ecb_enc(nonce+struct.pack("<Q",offset),key)
	new_block = xor(new_block,plaintext)
	ciph = ciph[:offset*16] + new_block + ciph[offset*16+16:]
	
def decrypt():
	plain = b''
	for i in range(0,len(ciph)//16):
		old = ciph[i*16:i*16+16]
		edit(i,b'\x00'*16)
		new = ciph[i*16:i*16+16]
		plain += xor(old,new)
	return plain
	
print(decrypt())
#print(decrypt())