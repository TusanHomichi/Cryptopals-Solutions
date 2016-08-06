from matasano import *

k = 768
e,d,n = gen_rsa(k)
B = 2**(k-16)
calls = 0
def oracle(m):
	global d,n,B,calls
	calls += 1
	m = pow(m,d,n)
	return 2*B <= m and m < 3*B
	
#Step 3
def union(M):
	newM = []
	M = sorted(M)
	i = 0
	right = M[0][1]
	while i < len(M):
		j = i+1
		while j < len(M) and M[j][0] < right:
			right = max(right,M[j][1])
			j += 1
		newM.append((M[i][0],right))
		i = j
	return newM

def update(M,s):
	global B,n
	newM = []
	for a,b in M:
		for r in range((a*s-3*B+1)//n, (b*s-2*B)//n + 1):
			newa = max(a,(2*B+r*n+s-1)//s)
			newb = min(b,(3*B-1+r*n)//s)
			if newa <= newb:
				newM.append((newa,newb))
	return newM

msg = b'Hello!'
plain = bytes2int(pkcs15_pad(msg,k))
ciph = pow(plain,e,n)
M = [(2*B,3*B-1)]
s = n//(3*B)

def check(M):
	global plain
	for a,b in M:
		if a <= plain and plain <= b:
			return True
	return False


#Step 2a
print("Initial search")
while not oracle(pow(s,e,n)*ciph):
	s += 1
M = update(M,s)

#Step 2b
print("Reducing intervals")
while len(M) > 1:
	print("\tDown to %d intervals" % len(M))
	s += 1
	while not oracle(pow(s,e,n)*ciph):
		s += 1
	M = update(M,s)
	
#Step 2c
print("Reducing length")
while M[0][1] - M[0][0] > 0:
	print("\tDown to 2^%d in %d calls" % (len(bin(M[0][1]-M[0][0]))-2,calls))
	r = 2*(M[0][1]*s-2*B+n-1)//n
	found = False
	while not found:
		for s in range((2*B+r*n+M[0][1]-1)//M[0][1], (3*B+r*n)//M[0][0]+1):
			if oracle(pow(s,e,n)*ciph):
				found = True
				break
		r += 1
	M = update(M,s)
	assert(check(M))

broken = M[0][0]
assert(broken == plain)