from matasano import *

ec = EC_M(233970423115425145524320034830162017933,534,1,4,order=233970423115425145498902418297807005944)
assert(ec.scale(4,ec.order) == 0)

aPriv = randint(1,ec.order-1)
aPub = ec.scale(4,aPriv)

print("Factoring...")
twist_ord = 2*ec.prime+2 - ec.order
factors = []
x = twist_ord
for i in range(2,2**24):
	if x%i == 0:
		if x%(i*i) != 0:
			factors.append(i)
		x = pp(x,i)
		
print("Getting remainders...")
rems = []
for f in factors:
	u = 0
	while u == 0:
		while isQRes((u**3+ec.A*u**2+u)%ec.prime,ec.prime):
			u = randint(1,ec.prime-1)
		u = ec.scale(u,pp(twist_ord,f))
	while ec.scale(u,f) != 0:
		u = ec.scale(u,f)
	shared = ec.scale(u,aPriv)	#Not generating the MAC this time
	for i in range(f):
		if ec.scale(u,i) == shared:
			print("\tSolved mod %d"%f)
			rems.append(i)
			break

#Now aPriv is +-rems[i] mod factors[i]
#Do them 2 at a time to get down to 2 values mod Prod factors[i]
print("Correcting parities...")
for i in range(len(factors)):
	if rems[i] != 0:
		break
fixed = i
for i in range(len(factors)):
	if i == fixed:
		continue
	u = 0
	while u == 0:
		while isQRes((u**3+ec.A*u**2+u)%ec.prime,ec.prime):
			u = randint(1,ec.prime-1)
		u = ec.scale(u,pp(pp(twist_ord,factors[fixed]),factors[i]))
		if ec.scale(u,factors[fixed]) == 0:
			u = 0
		elif ec.scale(u,factors[i]) == 0:
			u = 0
	shared = ec.scale(u,aPriv)
	r,_ = crt([rems[fixed],rems[i]],[factors[fixed],factors[i]])
	if ec.scale(u,r) != shared:
		rems[i] = (-rems[i])%factors[i]
		
#Now I need to run down the remaining bits
