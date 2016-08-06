from matasano import *
from os import urandom

key = urandom(16)

def gen(b):
	return aes_cbc_enc(pkcs7_pad(b"comment1=cooking%20MCs;userdata=" + b + b";comment2=%20like%20a%20pound%20of%20bacon",16), key, key)	#Key as IV
	
def check(b):
	b = aes_cbc_dec(b,key,key)
	for x in b:
		if x >= 128:
			return (False,b)
	return (True,b"")
	
def get_key():
	tok = gen(b"\x00"*48)[:48]
	v,x = check(tok[:16] + b'\x00'*16 + tok[:16])
	if not v:
		return xor(x[:16],x[32:48])
	
print("Actual key: %s" % key)
print("Found key: %s" % get_key())