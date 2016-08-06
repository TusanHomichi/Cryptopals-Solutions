from matasano import *

size = 2
def my_hash(m,iv=None):
	if not iv:
		h = b"\x00"*size
	else:
		h = iv
	key = b"\x00"*16
	for i in range(0,len(m),size):
		h = aes_ecb_enc(h+m[i:i+size]+b"\x00"*(16-2*size),key)[:size]
	return h
	
def get_collision(h0,h1):
	found0 = {}
	found1 = {}
	while True:
		m = randbytes(size)
		h = my_hash(m,iv=h0)
		found0[h] = m
		h = my_hash(m,iv=h1)
		found1[h] = m
		
		if h in found0 and h in found1:
			return found0[h], found1[h]

def get_funnel(k):
	leaves = [randbytes(size) for i in range(2**k)]
	tree = {}
	while len(leaves) > 1:
		h0 = leaves[0]
		h1 = leaves[1]
		m0,m1 = get_collision(h0,h1)
		tree[h0] = m0
		tree[h1] = m1
		leaves.pop()
		leaves.pop()
		leaves.append(my_hash(m0,iv=h0))
	tree[leaves[0]] = b""
	return (tree,leaves[0])
	
funnel,end = get_funnel(6)
print("I predict the hash will be %s" % end)

print("What should the message be?")
msg = input().encode('ascii')
hash = my_hash(msg+b"\x00"*((size-len(msg))%size))
glue = randbytes(size)
while my_hash(glue,iv=hash) not in funnel:
	glue = randbytes(size)

padded = msg + b"\x00"*((size-len(msg))%size) + glue
while len(funnel[my_hash(padded)]) > 0:
	padded += funnel[my_hash(padded)]

print("The message is: %s" % padded)
print("And behold! The hash is: %s" % my_hash(padded))