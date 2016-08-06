from matasano import *

p = 0x800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1
q = 0xf4f47f05794b256174bba6e9b396a7707e563c5b
params = (p,q,0)

key = gen_dsa_key(params)
pub = 0x2d026f4bf30195ede3a088da85e398ef869611d0f68f0713d51c9c1a3a26c95105d915e2d8cdf26d056b86b8a7b85519b1c23cc3ecdc6062650462e3063bd179c2a6581519f674a61f1d89a1fff27171ebc1b93d4dc57bceb7ae2430f98a6a4d83d8279ee65d71c1203d2c96d65ebbf7cce9d32971c3de5084cce04a2e147821


msg = b'Hello!'
print("g=0")
sig = (0,bytes2int(hash(msg,sha1)))
print("Forged signature for %s = %s" % (msg,sig))
print("Forged signature verifies: %s" % dsa_verify(msg,sig,key[1],params,sha1)) 
print()

print("g=p+1")
params = (p,q,p+1)
key = gen_dsa_key(params)
sig = (1,1)
print("Forged signature for all messages: (%d,%d)" % sig)
print("Forged signature verifies on %s: %s" % (b'Hello!',dsa_verify(msg,sig,key[1],params,sha1)))
print("Forged signature verifies on %s: %s" % (b'Hello, world!',dsa_verify(msg,sig,key[1],params,sha1)))
print("Forged signature verifies on %s: %s" % (b'Goodbye, world',dsa_verify(msg,sig,key[1],params,sha1)))
print()