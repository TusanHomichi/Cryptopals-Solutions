from matasano import *

def dh(p=37,g=5):
	a = randint(0,p-1)
	A = pow(g,a,p)
	print("A chooses %d as private key, giving %d as public key" % (a,A))
	b = randint(0,p-1)
	B = pow(g,b,p)
	print("B chooses %d as private key, giving %d as public key" % (b,B))
	print("Session key: %s" % bytes2hex(hash(int2bytes(pow(A,b,p)),sha1)))
	return pow(A,b,p)

dh()	
