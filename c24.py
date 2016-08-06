from matasano import *
from struct import pack

def mt19937_cipher(plain,seed):
	r = mt19937(seed)
	stream = bytes([])
	while len(stream) < len(plain):
		x = r.rand()
		stream += pack("<L",x)
	return xor(plain,stream)
	
#Brute force the seed, not bothering

#Just use the cipher for tokens