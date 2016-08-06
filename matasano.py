from base64 import b64encode
import random
import os
import pyaes
import struct
import hashlib

def hex2bytes(s):
	return bytes([int(s[i:i+2],16) for i in range(0,len(s),2)])

def hex2b64(s):
	return b64encode(hex2bytes(s))
	
def bytes2hex(b):
	return "".join(["%02x" % x for x in b])
	
def b642hex(s):
	return bytes2hex(b64decode(s))
	
def int2hex(n):
	s = hex(n).replace('0x','').replace('L','')	
	if len(s) % 2 == 1:
		s = '0' + s
	return s
	
def int2bytes(n):
	return hex2bytes(int2hex(n))
	
def bytes2int(b):
	return int(bytes2hex(b),16)
	
def xor(a,b):
	return bytes([a[i] ^ b[i] for i in range(min(len(a),len(b)))])
	
def rep_xor(a,b):
	return bytes([a[i%len(a)] ^ b[i%len(b)] for i in range(max(len(a),len(b)))])
	
def freq(l):
	freqs = {}
	for x in l:
		if x not in freqs:
			freqs[x] = 0
		freqs[x] += 1
	return freqs
	
def unigram(s):
	return freq(list(s))
	
def bigram(s):
	return freq([s[i:i+2] for i in range(0,len(s),2)])
	
def trigram(s):
	return freq([s[i:i+3] for i in range(0,len(s),3)])
	
def ks_score(sample,ref):
	size = sum([sample[x] for x in sample])
	sample = {x:sample[x]/size for x in sample}
	un = [x for x in sample]
	for x in ref:
		if x not in un:
			un.append(x)
	un = sorted(un)
	diff = [0]
	for x in un:
		if x in sample:
			diff.append(diff[-1]+sample[x])
		else:
			diff.append(diff[-1])

		if x in ref:
			diff[-1] -= ref[x]
	return max(abs(max(diff)), abs(min(diff)))
	
def chi2score(s1,s2):
	sz1 = sum([s1[i] for i in s1])
	sz2 = sum([s2[i] for i in s2])
	k1 = (sz2/sz1)**0.5
	k2 = (sz1/sz2)**0.5
	un = [x for x in s1]
	for x in s2:
		if x not in un:
			un.append(x)
	un = sorted(un)	
	tot = 0
	for x in un:
		c1 = 0
		if x in s1:
			c1 = s1[x]
		c2 = 0
		if x in s2:
			c2 = s2[x]
		tot += (k1*c1-k2*c2)**2/(c1+c2)
	return tot
	
def is_ascii(b):
	for x in b:
		if x >= 128:
			return False
	return True
	
def is_letter(c):
	alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz .,'"
	return chr(c) in alph
	
def letter_cnt(b):
	ct = 0
	for x in b:
		if is_letter(x):
			ct += 1
	return ct
	
def bits(i):
	tot = 0
	while i > 0:
		if i%2 == 1:
			tot += 1
		i //= 2
	return tot
	
def hamming(b1,b2):
	tot = 0
	for i in range(max(len(b1),len(b2))):
		c1 = 0
		if i < len(b1):
			c1 = b1[i]
		c2 = 0
		if i < len(b2):
			c2 = b2[i]
		tot += bits(c1^c2)
	return tot
	
uni_freq = [0.0812, 0.0149, 0.0271, 0.0432, 0.1203, 0.023, 0.0203, 0.0592, 0.0731, 0.001, 0.0069, 0.0398, 0.0261, 0.0695, 0.0768, 0.0182, 0.0011, 0.0602, 0.0628, 0.091, 0.0288, 0.0111, 0.0209, 0.0017, 0.0211, 0.0007]
uni_freq = {i+ord('a'):uni_freq[i] for i in range(26)}

def aes_ecb_enc(plain,key):
	aes = pyaes.AES(key)
	ciph = []
	for i in range(0,len(plain),16):
		ciph += aes.encrypt(plain[i:i+16])
	return bytes(ciph)
	
def aes_ecb_dec(ciph,key):
	aes = pyaes.AES(key)
	plain = []
	for i in range(0,len(ciph),16):
		plain += aes.decrypt(ciph[i:i+16])
	return bytes(plain)
	
def pkcs7_pad(b, sz=16):
	toAdd = sz - (len(b)%sz)
	return bytes(list(b)+[toAdd]*toAdd)
	
def pkcs7_unpad(b):
	pad = b[-b[-1]:]
	if pad != bytes([b[-1]]*b[-1]):
		raise Exception("Bad padding")
	return b[:-b[-1]]
	
def aes_cbc_enc(plain, key, iv):
	aes = pyaes.AESModeOfOperationCBC(key, iv=iv)
	ciph = []
	for i in range(0,len(plain),16):
		ciph += aes.encrypt(plain[i:i+16])
	return bytes(ciph)
	
def aes_cbc_dec(ciph, key, iv):
	aes = pyaes.AESModeOfOperationCBC(key, iv=iv)
	plain = []
	for i in range(0,len(ciph),16):
		plain += aes.decrypt(ciph[i:i+16])
	return bytes(plain)
	
def randbytes(l):
	return os.urandom(l)
	
def randint(a,b=None):
	if b:
		return random.randint(a,b)
	else:
		return random.randint(0,a)
	
def aes_ctr(text,key,nonce):
	stream = bytes([])
	i = 0
	while len(stream) < len(text):
		stream += aes_ecb_enc(nonce+struct.pack("<Q",i), key)
		i += 1
	return xor(text,stream)
	
class mt19937:
	w,n,m,r = 32,624,397,31
	lower = (1<<r) - 1
	upper = 0xFFFFFFFF ^ lower
	size = (1<<w) - 1

	a = 0x9908B0DF
	u,d = 11,0xFFFFFFFF
	s,b = 7, 0x9D2C5680
	t,c = 15,0xEFC60000
	l = 18
	
	f = 1812433253
		
	def seed(self, i):
		self.state[0] = i
		for i in range(self.n):
			self.state[i] = (self.f*(self.state[i-1] ^ (self.state[i-1] >> (self.w-2))) + i) & self.size

	def __init__(self, seed):
		self.state = [0]*self.n
		self.seed(seed)
		
	def rand(self):
		#Update state
		x = (self.state[0]&self.upper) + (self.state[1]&self.lower)
		if x%2 != 0:
			x = (x >> 1) ^ self.state[self.m]
			x = x ^ self.a
		else:
			x = (x >> 1) ^ self.state[self.m]
			
		self.state.append(x & self.size)
		self.state.pop(0)
		
		#Temper
		y = x ^ ((x>>self.u) & self.d)
		y = y ^ ((y<<self.s) & self.b)
		y = y ^ ((y<<self.t) & self.c)
		y = y ^ (y >> self.l)
		return y & self.size

def keyed_mac(text, key, hash):
	hash.update(key+text)
	return hash.digest()
	
class md4:
	block_size = 64
	hash_size = 16
		
	def __init__(self,a=0x67452301,b=0xefcdab89,c=0x98badcfe,d=0x10325476):	
		self.a = a
		self.b = b
		self.c = c
		self.d = d
		
	def F(x,y,z):
		return (x&y) | (~x & z)
		
	def G(x,y,z):
		return (x&y) | (x&z) | (y&z)
		
	def H(x,y,z):
		return x^y^z
		
	def RotL(x,k):
		return ((x<<k) | (x>>(32-k))) & (2**32-1)
		
	def Op(a,b,c,d,xk,s,fun,imm):
		return md4.RotL((a+fun(b,c,d)+xk+imm)%(2**32),s)
		
	m = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15, 0,4,8,12,1,5,9,13,2,6,10,14,3,7,11,15, 0,8,4,12,2,10,6,14,1,9,5,13,3,11,7,15]
	shift = [3,7,11,19,3,7,11,19,3,7,11,19,3,7,11,19, 3,5,9,13,3,5,9,13,3,5,9,13,3,5,9,13, 3,9,11,15,3,9,11,15,3,9,11,15,3,9,11,15]
	rot = [0,0x5A827999,0x6ED9EBA1]
	phi = [F,G,H]
	def Round(a,b,c,d,x):
		for j in range(3):
			for i in range(4):
				a = md4.Op(a,b,c,d,x[md4.m[16*j+4*i]],md4.shift[16*j+4*i],md4.phi[j],md4.rot[j])
				d = md4.Op(d,a,b,c,x[md4.m[16*j+4*i+1]],md4.shift[16*j+4*i+1],md4.phi[j],md4.rot[j])
				c = md4.Op(c,d,a,b,x[md4.m[16*j+4*i+2]],md4.shift[16*j+4*i+2],md4.phi[j],md4.rot[j])
				b = md4.Op(b,c,d,a,x[md4.m[16*j+4*i+3]],md4.shift[16*j+4*i+3],md4.phi[j],md4.rot[j])
		return a,b,c,d
	
	def update(self,s,pref_len=0):
		sl = 8*len(s)+8*pref_len
		s += b'\x80'
		while len(s)%64 != 56:
			s += b'\x00'
		s += struct.pack("<Q",sl)
		sl = len(s)
		for block in range(0,sl,64):
			m = [0]*16
			for i in range(16):
				word = s[block+4*i:block+4*i+4]
				m[i] = word[0] + word[1]*256 + word[2]*256**2 + word[3]*256**3
			x,y,z,w = md4.Round(self.a,self.b,self.c,self.d,m)
			self.a = (self.a+x)%(2**32)
			self.b = (self.b+y)%(2**32)
			self.c = (self.c+z)%(2**32)
			self.d = (self.d+w)%(2**32)
			
	def digest(self):
		return struct.pack("<LLLL",self.a,self.b,self.c,self.d)
		
class sha1:
	block_size = 64
	hash_size = 20

	def __init__(self,h0=0x67452301,h1=0xEFCDAB89,h2=0x98BADCFE,h3=0x10325476,h4=0xC3D2E1F0):
		self.h0 = h0
		self.h1 = h1
		self.h2 = h2
		self.h3 = h3
		self.h4 = h4
		
	def RotL(self,x,k):
		x = x % 2**32
		return ((x<<k) | (x>>(32-k)))%2**32
		
	def Round(self,a,b,c,d,e,w):
		for i in range(80):
			if i < 20:
				f = (b & c) | (~b & d)
				k = 0x5A827999
			elif i < 40:
				f = b^c^d
				k = 0x6ED9EBA1
			elif i < 60:
				f = (b&c) | (b&d) | (c&d)
				k = 0x8F1BBCDC
			else:
				f = b^c^d
				k = 0xCA62C1D6
				
			tmp = (self.RotL(a,5)+f+e+k+w[i])%2**32
			e = d
			d = c
			c = self.RotL(b,30)
			b = a
			a = tmp
		return a,b,c,d,e
		
	def update(self,s,pref_len=0):
		sl = 8*len(s)+8*pref_len
		s += b'\x80'
		while len(s)%64 != 56:
			s += b'\x00'
		s += struct.pack(">Q",sl)
		for block in range(0,len(s),64):
			w = [0]*80
			for i in range(16):
				x = s[block+4*i:block+4*i+4]
				w[i] = x[0]*256**3 + x[1]*256**2 + x[2]*256 + x[3]
			for i in range(16,80):
				w[i] = self.RotL(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16],1)
			a,b,c,d,e = self.Round(self.h0,self.h1,self.h2,self.h3,self.h4,w)
			self.h0 = (self.h0+a)%2**32
			self.h1 = (self.h1+b)%2**32
			self.h2 = (self.h2+c)%2**32
			self.h3 = (self.h3+d)%2**32
			self.h4 = (self.h4+e)%2**32
	
	def digest(self):
		return struct.pack(">LLLLL",self.h0,self.h1,self.h2,self.h3,self.h4)
		return struct.pack(">LLLLL",self.h0,self.h1,self.h2,self.h3,self.h4)

def hash(s,h):
	h = h()
	h.update(s)
	return h.digest()

def hmac(k,m,h):
	if len(k) < h.block_size:
		k += b'\x00'*(h.block_size-len(k))
	elif len(k) > h.block_size:
		hash(k,h)
	opad = b'\x5c'*h.block_size
	ipad = b'\x36'*h.block_size
	return hash(xor(k,opad)+hash(xor(k,ipad)+m,h),h)

class sha256:
	block_size = 64
	hash_size = 32
	
	k = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070, 0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]
	
	def __init__(self, h0 = 0x6a09e667, h1 = 0xbb67ae85, h2 = 0x3c6ef372, h3 = 0xa54ff53a, h4 = 0x510e527f, h5 = 0x9b05688c, h6 = 0x1f83d9ab, h7 = 0x5be0cd19):
		self.h0 = h0
		self.h1 = h1
		self.h2 = h2
		self.h3 = h3
		self.h4 = h4
		self.h5 = h5
		self.h6 = h6
		self.h7 = h7
		
	def RotR(self,x,k):
		return (x>>k | x << (32-k)) % 2**32
		
	def Round(self,a,b,c,d,e,f,g,h,w):
		for i in range(64):
			s1 = self.RotR(e,6) ^ self.RotR(e,11) ^ self.RotR(e,25)
			ch = (e & f) ^ (~e & g)
			temp1 = (h+s1+ch+self.k[i]+w[i])%2**32
			s0 = self.RotR(a,2) ^ self.RotR(a,13) ^ self.RotR(a,22)
			maj = (a&b) ^ (a&c) ^ (b&c)
			temp2 = (s0+maj)%2**32
			
			h=g
			g=f
			f=e
			e=(d+temp1)%2**32
			d=c
			c=b
			b=a
			a=(temp1+temp2)%2**32
		return a,b,c,d,e,f,g,h
		
	def update(self,s,pref_len=0):
		sl = 8*len(s) + 8*pref_len
		s += b'\x80'
		while len(s)%64 != 56:
			s += b'\x00'
		s += struct.pack(">Q",sl)
		for block in range(0,len(s),64):
			w = [0]*64
			for i in range(16):
				x = s[block+4*i:block+4*i+4]
				w[i] = x[0]*256**3 + x[1]*256**2 + x[2]*256 + x[3]
			for i in range(16,64):
				s0 = self.RotR(w[i-15],7) ^ self.RotR(w[i-15],18) ^ (w[i-15] >> 3)
				s1 = self.RotR(w[i-2],17) ^ self.RotR(w[i-2],19) ^ (w[i-2] >> 10)
				w[i] = (w[i-16] + s0 + w[i-7] + s1) % 2**32
			a,b,c,d,e,f,g,h = self.Round(self.h0,self.h1,self.h2,self.h3,self.h4,self.h5,self.h6,self.h7,w)
			self.h0 = (self.h0+a)%2**32
			self.h1 = (self.h1+b)%2**32
			self.h2 = (self.h2+c)%2**32
			self.h3 = (self.h3+d)%2**32
			self.h4 = (self.h4+e)%2**32
			self.h5 = (self.h5+f)%2**32
			self.h6 = (self.h6+g)%2**32
			self.h7 = (self.h7+h)%2**32
	
	def digest(self):
		return struct.pack(">LLLLLLLL",self.h0,self.h1,self.h2,self.h3,self.h4,self.h5,self.h6,self.h7)

class Connection:
	def __init__(self,a,b):
		self.a = a
		self.b = b
		self.a.conn = self
		self.b.conn = self
		self.qab = []
		self.qba = []

	def Done(self):
		return len(self.qab) == 0 and len(self.qba) == 0
	
	def Update(self):
		if len(self.qab) > 0:
			msg = self.qab.pop()
			print("Send %r from %r to %r" % (msg,type(self.a).__name__,type(self.b).__name__))
			self.b.OnRecv(msg)
		if len(self.qba) > 0:
			msg = self.qba.pop()
			print("Send %r from %r to %r" % (msg,type(self.b).__name__,type(self.a).__name__))
			self.a.OnRecv(msg)
			
	def Send(self,msg,src):
		if src == self.a:
			self.qab.append(msg)
		if src == self.b:
			self.qba.append(msg)

def trial_div(n):
	if n%2 == 0:
		return n == 2
	d=3
	while d*d <= n:
		if n%d == 0:
			return d
		d += 2
	return None
			
def mr_round(n,r,s):
	x = pow(randint(1,n-1),s,n)
	for i in range(r):
		x = (x*x)%n
		if x == 1:
			return True
	return False
			
def miller_rabin(n,t):
	if n%2 == 0:
		return n == 2
	r = 0
	s = n-1
	while s%2 == 0:
		s //= 2
		r += 1
	for i in range(t):
		if not mr_round(n,r,s):
			return False
	return True
	
def xgcd(x,y):
	if x > y:
		g,a,b = xgcd(y,x)
		return g,b,a
	if x == 0:
		return y,0,1
	q,r = y//x, y%x
	g,a,b = xgcd(r,x)
	return g,b-q*a,a
	
def inv(i,n):
	return xgcd(i%n,n)[1]%n
	
def gcd(a,b):
	return xgcd(a,b)[0]
	
def crt(rems,mods):
	prod = 1
	for m in mods:
		prod *= m
	ret = 0
	for i in range(len(mods)):
		ret += rems[i]*prod//mods[i]*inv(prod//mods[i],mods[i])
	return ret%prod,prod
	
#Make a prime that is rem mod mod and is bits bits long
#Will loop forever if you force divisibility
def gen_prime(bits,rem=1,mod=2):
	p = mod*randint(2**(bits-1)//mod,(2**bits-1)//mod)+rem
	while not miller_rabin(p,100):
		p = mod*randint(2**(bits-1)//mod,(2**bits-1)//mod)+rem
	return p
	
def gen_rsa(bits,e=65537):
	d,p,q = 0,0,0
	while (e*d)%((p-1)*(q-1)) != 1 or len(bin(p*q))-2 != bits or p == q:
		p = gen_prime(bits//2)
		q = gen_prime(bits//2)
		d = inv(e,(p-1)*(q-1))
	return (e,d,p*q)
	
def gen_dsa_params(N=40,L=256):
	q = gen_prime(N)
	p = gen_prime(L,1,q)
	h = 2
	g = pow(h,(p-1)//q,p)
	while g == 1:
		h = randint(2,p-1)
		g = pow(h,(p-1)//q,p)
	return p,q,g
	
def gen_dsa_key(params):
	p,q,g = params
	x = randint(1,q-1)
	y = pow(g,x,p)
	return x,y
	
def dsa_sign(m,priv,params,h):
	p,q,g = params
	k = randint(1,q-1)
	r = pow(g,k,p)%q
	while r == 0:
		k = randint(1,q-1)
		r = pow(g,k,p)%q
	s = (inv(k,q)*(bytes2int(hash(m,h))+priv*r))%q
	return r,s
	
def dsa_verify(m,sig,pub,params,h):
	r,s = sig
	p,q,g = params
	w = inv(s,q)
	u1 = (bytes2int(hash(m,h))*w)%q
	u2 = (r*w)%q
	v = ((pow(g,u1,p)*pow(pub,u2,p))%p)%q
	return v == r
	
def pkcs15_pad(b,n):
	return b'\x00\x02' + b'\xff'*(n//8-3-len(b)) + b'\x00' + b
	
def pkcs15_unpad(b):
	dat = b[1:].find(0)+1
	if b[0] != 0 or b[1] != 2 or dat == 0:
		raise Exception("Bad padding")
	return b[dat:]
	
def cbc_mac(msg, key, iv):
	return aes_cbc_enc(pkcs7_pad(msg),key,iv)[-16:]
	
def cbc_mac_verify(msg,key,iv,mac):
	return cbc_mac(msg,key,iv) == mac
	
def rc4(key,n):
	S = [i for i in range(256)]
	j = 0
	for i in range(256):
		j = (j+S[i]+key[i%len(key)])%256
		tmp = S[i]
		S[i] = S[j]
		S[j] = tmp
	ret = b""	
	i = 0
	j = 0
	while len(ret) < n:
		i = (i+1)%256
		j = (j+S[i])%256
		tmp = S[i]
		S[i] = S[j]
		S[j] = tmp
		K = S[(S[i]+S[j])%256]
		ret += bytes([K])
	return ret

#Code written for set 8	
import math
def pollard_lambda_mod(y,a,b,g,p):
	k = int(math.log(b-a)/math.log(4))
	N = 4*(2**k-1)//k
	while True:
		xT = 0
		yT = pow(g,b,p)
		for i in range(N):
			step = 2**(yT%k)
			xT += step
			yT = (yT*pow(g,step,p))%p
		xW = 0
		yW = y
		while xW < b-a+xT:
			step = 2**(yW%k)
			xW += step
			yW = (yW*pow(g,step,p))%p
			
			if yW == yT:
				return b+xT-xW
		N *= 2
		
def pp(n,p):
	while n%p == 0:
		n //= p
	return n
		
class EC_WS:	#Weierstrass form
	def __init__(self,p,a,b,base_x,base_y,order=-1):	#Don't always need the order
		self.prime = p
		self.a = a
		self.b = b
		self.g = (base_x,base_y)
		self.order = order
		
	def add(self,p,q):
		if p == (0,1):
			return q
			
		if q == (0,1):
			return p
			
		if p[0] == q[0]:
			if p[1] == (-q[1])%self.prime:
				return (0,1)
			else:
				m = ((3*p[0]*p[0]+self.a)*inv(2*p[1],self.prime))%self.prime
		else:
			m = ((q[1]-p[1])*inv(q[0]-p[0],self.prime))%self.prime
			
		x3 = (m*m-p[0]-q[0])%self.prime
		y3 = (m*(p[0]-x3)-p[1])%self.prime
				
		return (x3,y3)
		
	def scale(self,p,n):
		ret = (0,1)
		while n > 0:
			if n%2 == 1:
				ret = self.add(ret,p)
			p = self.add(p,p)
			n //= 2
		return ret
		
	def on_curve(self,p):
		return p==(0,1) or (p[1]**2-p[0]**3-self.a*p[0]-self.b)%self.prime == 0
		
def isQRes(n,p):
	return pow(n,(p-1)//2,p) != p-1

#Tonelli-Shanks, right off wikipedia
#Could probably be optimized
def mod_sqrt(n,p):
	assert(pow(n,(p-1)//2,p) == 1)
	Q = p-1
	S = 0
	while Q%2 == 0:
		S += 1
		Q //= 2
	z = 2
	while pow(z,(p-1)//2,p) == 1:
		z += 1
	c = pow(z,Q,p)
	R = pow(n,(Q+1)//2,p)
	t = pow(n,Q,p)
	M = S
	while True:
		if t == 1:
			return R
		i = 0
		old_t = t
		while t != 1:
			t = (t*t)%p
			i += 1
		b = pow(c,pow(2,(M-i-1),p-1),p)
		R = (R*b)%p
		t = (old_t*b*b)%p
		c = (b*b)%p
		M = i
		
class EC_M:
	def __init__(self,p,A,B,base_x,order=-1):
		self.prime = p
		self.A = A
		self.B = B
		self.base_x = base_x
		self.order = order
		
	def scale(self,x,n):
		u2,w2 = (1,0)
		u3,w3 = (x,1)
		for i in range(len(bin(self.prime))-3,-1,-1):
			b = 1 & (n>>i)
			u2,u3 = u2*(1-b)+u3*b,u2*b+u3*(1-b)
			w2,w3 = w2*(1-b)+w3*b,w2*b+w3*(1-b)
			u3,w3 = (u2*u3 - w2*w3)**2, x*(u2*w3 - w2*u3)**2
			u3,w3 = u3%self.prime, w3%self.prime
			u2,w2 = (u2**2 - w2**2)**2, 4*u2*w2 * (u2**2 + self.A*u2*w2 + w2**2)
			u2,w2 = u2%self.prime, w2%self.prime
			u2,u3 = u2*(1-b)+u3*b,u2*b+u3*(1-b)
			w2,w3 = w2*(1-b)+w3*b,w2*b+w3*(1-b)
		return (u2*pow(w2,self.prime-2,self.prime))%self.prime
		
def pollard_lambda_ec(y,a,b,ec):
	k = int(math.log(b-a)/math.log(4))
	N = 4*(2**k-1)//k
	while True:
		xT = 0
		yT = ec.scale(ec.base,b)
		for i in range(N):
			step = 2**(yT%k)
			xT += step
			yT = ec.scale(ec.base,b+xT)	#Kinda horrible, but I don't want to deal with the addition formulas
		xW = 0
		yW = y
		while xW < b-a+xT:
			step = 2**(yW%k)
			xW += step
			yW = (yW*pow(g,step,p))%p
			
			if yW == yT:
				return b+xT-xW
		N *= 2