from matasano import *

size = 2	#Size between 1 and 8
k = 7
M = randbytes(2**k*size)
def my_hash(m,iv=None):
	if not iv:
		h = b"\x00"*size
	else:
		h = iv
	key = b"\x00"*16
	for i in range(0,len(m),size):
		h = aes_ecb_enc(h+m[i:i+size]+b"\x00"*(16-2*size),key)[:size]
	return h
	
def get_collision(a,b,iv=None):
	dummy1 = b"\x00"*((a-1)*size)
	dummy2 = b"\x00"*((b-1)*size)
	a_iv = my_hash(dummy1,iv=iv)
	b_iv = my_hash(dummy2,iv=iv)
	a_found = {}
	b_found = {}
	while True:
		x = randbytes(size)
		h = my_hash(x,iv=a_iv)
		if h in b_found:
			return dummy1+x,dummy2+b_found[h]
		a_found[h] = x
		h = my_hash(x,iv=b_iv)
		if h in a_found:
			return dummy1+a_found[h],dummy2+x

def make_expandable(k):
	iv = None
	exp = []
	for i in range(1,k+1):
		exp.append(get_collision(1,2**(k-i)+1,iv=iv))
		iv = my_hash(exp[-1][0],iv=iv)
	return exp

intermediate = {}
last = b"\x00"*size
for i in range(0,len(M),size):
	last = my_hash(M[i:i+size],iv=last)
	intermediate[last] = i+size
	
exp = make_expandable(k)
iv = my_hash(b"".join([x[0] for x in exp]))
glue = randbytes(size)
h = my_hash(glue,iv=iv)
while h not in intermediate:
	glue = randbytes(size)
	h = my_hash(glue,iv=iv)
	
suff = glue + M[intermediate[h]:]
target = (len(M) - len(suff))//size - k
msg = suff
for i in range(k):
	msg = exp[k-i-1][(target>>i)&1] + msg
	
assert(len(M) == len(msg))
assert(my_hash(M) == my_hash(msg))
print("Constructed preimage!")