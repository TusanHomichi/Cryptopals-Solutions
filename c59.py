from matasano import *

p = 233970423115425145524320034830162017933
a = -95051
b = 11279326
g = (182,85518893674295321206118380980485522083)
order = 29246302889428143187362802287225875743
ec = EC_WS(p,a,b,g[0],g[1],order=order)

print("Checking EC operations...")
assert(ec.scale(g,order) == (0,1))
print("OK")

print("Alice-Bob exchange...")
aPriv = randint(1,order-1)
aPub = ec.scale(g,aPriv)

bPriv = randint(1,order-1)
bPub = ec.scale(g,bPriv)

assert(ec.scale(aPub,bPriv) == ec.scale(bPub,aPriv))
shared = ec.scale(aPub,bPriv)
print("Alice and Bob can talk!")

print("Eve-Bob exchanges")
curves = [(210,233970423115425145550826547352470124412),(504,233970423115425145544350131142039591210),(727,233970423115425145545378039958152057148)]
rems = []
factors = []
prod = 1
for new_b,new_ord in curves:
	ord_copy = new_ord
	for f in range(2,2**16):
		if prod > order:
			break
		if ord_copy%f == 0:
			ord_copy = pp(ord_copy,f)
			if f in factors:	#Don't repeat factors
				continue
			h = (0,1)		#Get point of order f
			while h == (0,1):
				h = randint(1,ec.prime-1)
				while not isQRes(h**3+ec.a*h+new_b,ec.prime):
					h = randint(1,ec.prime-1)
				h = (h,mod_sqrt(h**3+ec.a*h+new_b,ec.prime))
				h = ec.scale(h,pp(new_ord,f))
			while ec.scale(h,f) != (0,1):
				h = ec.scale(h,f)
			#Do exchange
			bShared = ec.scale(h,bPriv)
			mac = hmac(int2bytes(bShared[0])+int2bytes(bShared[1]),b"crazy flamboyant for the rap enjoyment",sha256)
			
			#Brute-force the remainder
			for i in range(f):
				testShared = ec.scale(h,i)
				if hmac(int2bytes(testShared[0])+int2bytes(testShared[1]),b"crazy flamboyant for the rap enjoyment",sha256) == mac:
					rems.append(i)
					factors.append(f)
					prod *= f
					print("\tSolved mod %d"%f)
					break
		
rem,prod = crt(rems,factors)
assert(prod > order)
assert(rem == bPriv)
print("Eve recovered %d, which matches Bob's private key" % rem)