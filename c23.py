from matasano import *

#Inverts y = x^((x>>a) & b)
def right_inv(y,a,b):
	bits = [0]*mt19937.w
	for i in range(mt19937.w-1,-1,-1):
		bits[i] = (y>>i)&1
		if i+a < len(bits):
			bits[i] ^= bits[i+a] & (b>>i) & 1
	ret = 0
	for i in range(mt19937.w-1,-1,-1):
		ret *= 2
		ret += bits[i]
	return ret
	
#Inverts y = x^((x<<a)&b)
def left_inv(y,a,b):
	bits = [0]*mt19937.w
	for i in range(mt19937.w):
		bits[i] = (y>>i)&1
		if i-a >= 0:
			bits[i] ^= bits[i-a] & (b>>i) & 1
	ret = 0
	for i in range(mt19937.w-1,-1,-1):
		ret *= 2
		ret += bits[i]
	return ret
	
def temper(x):
	y = x ^ ((x>>mt19937.u) & mt19937.d)
	y = y ^ ((y<<mt19937.s) & mt19937.b)
	y = y ^ ((y<<mt19937.t) & mt19937.c)
	y = y ^ (y >> mt19937.l)
	return y & mt19937.size
	
def untemper(y):
	y = right_inv(y, mt19937.l, mt19937.size)
	y = left_inv(y, mt19937.t, mt19937.c)
	y = left_inv(y, mt19937.s, mt19937.b)
	y = right_inv(y, mt19937.u, mt19937.d)
	return y
	
r = mt19937(randint(0,2**32-1))
output = []
for i in range(624):
	output.append(r.rand())
	
clone = mt19937(0)
for i in range(624):
	clone.state[i] = untemper(output[i])
	
for i in range(1000):
	assert(clone.rand() == r.rand())
	
print("Success!")