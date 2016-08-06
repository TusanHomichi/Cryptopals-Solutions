from matasano import *

p = 7199773997391911030609999317773941274322764333428698921736339643928346453700085358802973900485592910475480089726140708102474957429903531369589969318716771
g = 4565356397095740655436854503483826832136106141639563487732438195343690437606117828318042418238184896212352329118608100083187535033402010599512641674644143
q = 236234353446506858198510045061214171961

assert((p-1)%q == 0)
j = (p-1)//q

#Alice-Bob Exchange
print("Alice-Bob exchange...")
aPriv = randint(1,q-1)
aPub = pow(g,aPriv,p)

bPriv = randint(1,q-1)
bPub = pow(g,bPriv,p)

assert(pow(aPub,bPriv,p) == pow(bPub,aPriv,p))
shared = pow(aPub,bPriv,p)
print("Alice and Bob can talk!")

#Get some subgroups
print("Factoring...")
factors = []
i = 2
prod = 1
while prod < q:
	if j%i == 0:
		j = pp(j,i)
		factors.append(i)
		prod *= i
	i += 1

#Eve-Bob exchanges
print("Eve-Bob exchanges...")
rems = []
for f in factors:
	h = 1
	while h == 1:
		h = pow(randint(1,p-1),pp(p-1,f),p)
	while pow(h,f,p) != 1:
		h = pow(h,f,p)
	bShared = pow(h,bPriv,p)
	mac = hmac(int2bytes(bShared),b"crazy flamboyant for the rap enjoyment",sha256)
	for i in range(f):
		testShared = pow(h,i,p)
		if hmac(int2bytes(testShared),b"crazy flamboyant for the rap enjoyment",sha256) == mac:
			rems.append(i)
			print("\tSolved mod %d"%f)
			break

rem,prod = crt(rems,factors)
print("Eve knows Bob's private key is %d mod %d" % (rem,prod))
assert(prod > q)
print("She used enough factors that she knows his key is %d" % rem)
assert(bPriv == rem)
print("And she is correct!")