from matasano import *
from os import urandom

key = urandom(16)
iv = urandom(16)

def oracle(b):
	if b';' in b:
		return None
	elif b'=' in b:
		return None
	return aes_cbc_enc(pkcs7_pad(b"comment1=cooking%20MCs;userdata=" + b + b";comment2=%20like%20a%20pound%20of%20bacon",16), key, iv)
	
def parse(b):
	b = pkcs7_unpad(aes_cbc_dec(b,key,iv))
	ret = {}
	for x in b.split(b';'):
		if x.count(b'=') != 1:
			return None
		x = x.split(b'=')
		ret[x[0]] = x[1]
	return ret
	
def gen_admin():
	change = xor(b';comment2=%20l',b';admin=true;a=')
	tok = oracle(b'a'*16)	#The prefix is an integer multiple of blocks
	tok = xor(tok, b'\x00'*32+change+b'\x00'*(len(tok)-32-len(change)))
	return tok
	
print(parse(gen_admin()))