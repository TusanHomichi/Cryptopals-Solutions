from matasano import *

p = 11470374874925275658116663507232161402086650258453896274534991676898999262641581519101074740642369848233294239851519212341844337347119899874391456329785623
g = 622952335333961296978159266084741085889881358738459939978290179936063635566740258555167783009058567397963466103140082647486611657350811560630587013183357
q = 335062023296420808191071248367701059461
j = 34233586850807404623475048381328686211071196701374230492615844865929237417097514638999377942356150481334217896204702

assert((p-1)%q == 0)
j = (p-1)//q

#Example discrete logs
print("Computing example discrete logs...")
y = 7760073848032689505395005705677365876654629189298052775754597607446617558600394076764814236081991643094239886772481052254010323780165093955236429914607119
log = pollard_lambda_mod(y,0,2**20,g,p)
assert(pow(g,log,p) == y)
print("First log is %d" % log)
y = 9388897478013399550694114614498790691034187453089355259602614074132918843899833277397448144245883225611726912025846772975325932794909655215329941809013733
log = pollard_lambda_mod(y,0,2**20,g,p)
assert(pow(g,log,p) == y)
print("Second log is %d" % log)

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
for i in range(2,2**16):
	if j%i == 0:
		j = pp(j,i)
		factors.append(i)

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
new_pub = (bPub*inv(pow(g,rem,p),p))%p
m = pollard_lambda_mod(new_pub,0,(q-1)//prod+1,pow(g,prod,p),p)
print("And got the rest by Pollard's Kangaroos")
key = rem+m*prod
assert(key == bPriv)
print("Got key %d"%key)