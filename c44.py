from matasano import *

p = 0x800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1
q = 0xf4f47f05794b256174bba6e9b396a7707e563c5b
g = 0x5958c9d3898b224b12672c0b98e06c60df923cb8bc999d119458fef538b8fa4046c8db53039db620c094c9fa077ef389b5322a559946a71903f990f1f7e0e025e2d7f7cf494aff1a0470f5b64c36b625a097f1651fe775323556fe00b3608c887892878480e99041be601a62166ca6894bdd41a7054ec89f756ba9fc95302291
params = (p,q,g)

pub = 0x2d026f4bf30195ede3a088da85e398ef869611d0f68f0713d51c9c1a3a26c95105d915e2d8cdf26d056b86b8a7b85519b1c23cc3ecdc6062650462e3063bd179c2a6581519f674a61f1d89a1fff27171ebc1b93d4dc57bceb7ae2430f98a6a4d83d8279ee65d71c1203d2c96d65ebbf7cce9d32971c3de5084cce04a2e147821

msgs = []
hashes = []
sigs = []
file = open('c44.txt','r')
line = file.readline()
while len(line) > 0:
	msg = line[5:-1]
	s = int(file.readline()[3:-1])
	r = int(file.readline()[3:-1])
	m = int(file.readline()[3:-1],16)
	msgs.append(msg.encode('ascii'))
	sigs.append((r,s))
	line = file.readline()


for i in range(len(sigs)):
	for j in range(i):
		if sigs[i][0] == sigs[j][0]:
			k = ((bytes2int(hash(msgs[i],sha1)) - bytes2int(hash(msgs[j],sha1)))*inv(sigs[i][1]-sigs[j][1],q))%q
			print("Repeated nonce in %d and %d: %d" % (i,j,k))
			x = ((sigs[i][1]*k-bytes2int(hash(msgs[i],sha1)))*inv(sigs[i][0],q))%q
			print("Private key: %d" % x)
			break
		
assert(pow(g,x,p) == pub)
print("Keypair broken")