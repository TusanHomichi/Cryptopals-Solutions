from matasano import *
from os import urandom

def oracle(b):
	pref = urandom(10)
	suff = urandom(10)
	preflen = urandom(1)[0]%5+5
	sufflen = urandom(1)[0]%5+5
	s = pref[:preflen] + b + suff[:sufflen]
	if urandom(1)[0]%2 == 0:
		print("Chose ECB")
		return aes_ecb_enc(pkcs7_pad(s,16), urandom(16))
	else:
		print("Chose CBC")
		return aes_cbc_enc(pkcs7_pad(s,16), urandom(16), urandom(16))
		
def detect():
	b = bytes([ord('a')]*47)
	s = oracle(b)
	for i in range(16,len(s),16):
		if s[i:i+16] == s[i-16:i]:
			print("ECB detected")
			return
	print("CBC detected")
	
for i in range(10):
	detect()