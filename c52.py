from matasano import *

def my_hash(m,iv=None,size=2):	#Size between 1 and 8
	if not iv:
		h = b"\x00"*size
	else:
		h = iv
	key = b"\x00"*16
	for i in range(0,len(m),size):
		h = aes_ecb_enc(h+m[i:i+size]+b"\x00"*(16-2*size),key)[:size]
	return h
	
def find_block_collision(iv,sz):
	inv = {}
	x = randbytes(sz)
	h = my_hash(x,iv=iv,size=sz)
	while h not in inv or inv[h] == x:
		inv[h] = x
		x = randbytes(sz)
		h = my_hash(x,iv=iv,size=sz)
	return x,inv[h]
	
def find_collisions(n,sz):
	iv = b"\x00"*sz
	pairs = []
	while 2**len(pairs) < n:
		pairs.append(find_block_collision(iv,sz))
		iv = my_hash(pairs[-1][0],iv=iv,size=sz)
	collide = []
	for i in range(n):
		cur = b""
		for j in range(len(pairs)):
			cur += pairs[j][(i>>j)&1]
		collide.append(cur)
	return collide
	
def multi_collision_round(sz1,sz2):
	collide = find_collisions(2**(4*sz2),sz1)	#Sz is in bytes, so the bit length is 8*sz2
	inv = {}
	for x in collide:
		h = my_hash(x,size=sz2)
		if h not in inv:
			inv[h] = x
		else:
			return x,inv[h]
	return None
	
def multi_collision(sz1,sz2):
	x = multi_collision_round(sz1,sz2)
	while not x:
		x = multi_collision_round(sz1,sz2)
	return x
	
a,b = multi_collision(2,3)
assert(my_hash(a,size=2) == my_hash(b,size=2) and my_hash(a,size=3) == my_hash(b,size=3))
print("Found collision!")