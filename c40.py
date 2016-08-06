from matasano import *

def intCubeRoot(n):
	hi = 2
	while hi**3 < n:
		hi *= 2
	lo = hi//2

	while hi-lo > 10:
		mid = (hi+lo)//2
		if mid**3 > n:
			hi = mid
		elif mid**3 < n:
			lo = mid
		else:
			return mid

	while lo**3 <= n:
		lo += 1

	return lo-1

k1 = gen_rsa(256)
k2 = gen_rsa(256)
k3 = gen_rsa(256)

plain = bytes2int(b"Hello!")
c1 = pow(plain,k1[0],k1[2])
c2 = pow(plain,k2[0],k2[2])
c3 = pow(plain,k3[0],k3[2])

c = crt([c1,c2,c3],[k1[2],k2[2],k3[2]])
decrypted = intCubeRoot(c)
if plain==decrypted:
	print("It worked!")