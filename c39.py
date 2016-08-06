from matasano import *

p = gen_prime(256)
while p%3 == 1:
	p = gen_prime(256)

q = gen_prime(256)
while q%3 == 1:
	q = gen_prime(256)

n = p*q
e = 3
d = inv(e,(p-1)*(q-1))

for i in range(1,100):
	assert(pow(pow(i,e,n),d,n) == i)

print("RSA works!")