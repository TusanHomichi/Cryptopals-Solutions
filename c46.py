from matasano import *
from base64 import b64decode

def oracle(m):
	global d,n
	return pow(m,d,n)%2
	
def pretty_print(s):
	b = b''
	for c in s:
		if 32 <= c and c <= 126:
			b += bytes([c])
		else:
			b += bytes([randint(32,126)])
	print('\x1B[1A\x1B[2K%s'%b)

e,d,n = gen_rsa(1024)
#e,d,n = gen_rsa(10)
print("Key generated")

plain = "VGhhdCdzIHdoeSBJIGZvdW5kIHlvdSBkb24ndCBwbGF5IGFyb3VuZCB3aXRoIHRoZSBGdW5reSBDb2xkIE1lZGluYQ=="
plain = b64decode(plain)
#plain = bytes([65])

print('\x1B7')	#Save cursor position
ciph = pow(bytes2int(plain),e,n)
lo = 0
hi = n-1
while hi-lo > 0:
	i = 1
	while (hi*2**i)//n == (lo*2**i)//n:
		i += 1
	mid = n*((hi*2**i)//n)
	mid //= 2**i
	if oracle(ciph*pow(2,e*i,n)) == 1:
		lo = mid+1
	else:
		hi = mid
	
	pretty_print(int2bytes(hi))