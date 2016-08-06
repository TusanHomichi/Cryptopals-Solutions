from matasano import *

def int_cube_root(x):
	hi = 2
	while hi*hi*hi <= x:
		hi *= 2
	lo = hi//2

	while hi-lo > 1:
		mid = (hi+lo)//2
		if mid*mid*mid <= x:
			lo = mid
		elif mid*mid*mid > x:
			hi = mid

	return lo
	
e,d,n = gen_rsa(256,3)
def server(sig,m):
	global e,n
	sig = pow(sig,e,n)
	b = int2bytes(sig)
	i = b.find(m)
	if i == -1 or i < 4:
		return False
	if b[:1] != b'\x01' or b[i-1] != 0:	#Will lose the \x00 in conversion
		return False
	for j in range(2,i-1):
		if b[j] != 255:
			return False
	return True
	
def sign(h):
	global d,n
	m = b'\x00\x01\xff\x00' + h
	while bytes2int(b'\x00\x01\xff'+m[2:]) < n:
		m = b'\x00\x01\xff' + m[2:]
	return pow(bytes2int(m),d,n)

def fake_sign(h):
	global n
	b = b'\x00\x01' + b'\xff'*8 + b'\x00' + h
	while bytes2int(b+b'\xff') < n:
		b = b+b'\xff'
	return int_cube_root(bytes2int(b))

m = b'hi mom'
sig = sign(m)
print("Intended message signature: %s" % sig)
print("Signature verifies: %s" % server(sig,m))

fake = fake_sign(m)
print("Fake signature: %s" % fake)
print("Signature verifies: %s" % server(fake,m))