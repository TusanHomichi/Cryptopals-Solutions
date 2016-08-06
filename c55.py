from matasano import *

#This is pretty bad, it takes about ~70,000 attempts to find a collision
#There is really no documentation on this, especially on multi-step modifications
#But it works well enough to move on.

def bit(x,i):
	return (x>>(i-1))&1
	
def set(x,l):
	for i in l:
		x |= (1<<(i-1))
	return x
	
def clear(x,l):
	for i in l:
		x &= ~(1<<(i-1))
	return x
	
def eq(x,y,l):
	for i in l:
		x ^= (bit(x,i) ^ bit(y,i)) << (i-1)
	return x
	
def rotr(x,s):
	x = x%2**32
	return ((x>>s) | (x << (32-s)))%2**32
	
def rotl(x,s):
	x = x%2**32
	return ((x<<s) | (x >> (32-s)))%2**32

def get_m(a,b,c,d):
	m = [0]*16
	m[0] = (rotr(a[1],3) - a[0] - F(b[0],c[0],d[0]))%2**32
	m[1] = (rotr(d[1],7) - d[0] - F(a[1],b[0],c[0]))%2**32
	m[2] = (rotr(c[1],11) - c[0] - F(d[1],a[1],b[0]))%2**32
	m[3] = (rotr(b[1],19) - b[0] - F(c[1],d[1],a[1]))%2**32
	m[4] = (rotr(a[2],3) - a[1] - F(b[1],c[1],d[1]))%2**32
	m[5] = (rotr(d[2],7) - d[1] - F(a[2],b[1],c[1]))%2**32
	m[6] = (rotr(c[2],11) - c[1] - F(d[2],a[2],b[1]))%2**32
	m[7] = (rotr(b[2],19) - b[1] - F(c[2],d[2],a[2]))%2**32
	m[8] = (rotr(a[3],3) - a[2] - F(b[2],c[2],d[2]))%2**32
	m[9] = (rotr(d[3],7) - d[2] - F(a[3],b[2],c[2]))%2**32
	m[10] = (rotr(c[3],11) - c[2] - F(d[3],a[3],b[2]))%2**32
	m[11] = (rotr(b[3],19) - b[2] - F(c[3],d[3],a[3]))%2**32
	m[12] = (rotr(a[4],3) - a[3] - F(b[3],c[3],d[3]))%2**32
	m[13] = (rotr(d[4],7) - d[3] - F(a[4],b[3],c[3]))%2**32
	m[14] = (rotr(c[4],11) - c[3] - F(d[4],a[4],b[3]))%2**32
	m[15] = (rotr(b[4],19) - b[3] - F(c[4],d[4],a[4]))%2**32
	return m
	
#Really ugly and hand-coded, but I'm not sure I see a better way since there are so many weird conditions to match along the way
F = md4.F
G = md4.G
def attempt():
	m = [randint(2**32-1) for i in range(16)]
	m[1] &= ~(1<<31)
	m[2] &= ~(1<<31)
	m[2] |= (1<<28)
	m[12] |= (1<<16)
	
	a,b,c,d = [0]*13,[0]*13,[0]*13,[0]*13
	a[0],b[0],c[0],d[0] = 0x67452301,0xefcdab89,0x98badcfe,0x10325476
	
	#Single step modification to original message
	a[1] = rotl(a[0] + F(b[0],c[0],d[0]) + m[0], 3)
	a[1] = eq(a[1],b[0],[7])
	
	d[1] = rotl(d[0] + F(a[1],b[0],c[0]) + m[1], 7)
	d[1] = clear(d[1],[7])
	d[1] = eq(d[1],a[1],[8,11])

	c[1] = rotl(c[0] + F(d[1],a[1],b[0]) + m[2], 11)
	c[1] = set(c[1],[7,8])
	c[1] = clear(c[1],[11])
	c[1] = eq(c[1],d[1],[26])

	b[1] = rotl(b[0] + F(c[1],d[1],a[1]) + m[3], 19)
	b[1] = set(b[1],[7])
	b[1] = clear(b[1],[8,11,26])

	a[2] = rotl(a[1] + F(b[1],c[1],d[1]) + m[4], 3)
	a[2] = set(a[2],[8,11])
	a[2] = clear(a[2],[17,24,25,26])		#The 17,24,25 were added by me for multi-step
	a[2] = eq(a[2],b[1],[14])

	d[2] = rotl(d[1] + F(a[2],b[1],c[1]) + m[5], 7)
	d[2] = clear(d[2],[14])
	d[2] = eq(d[2],a[2],[19,20,21,22])
	d[2] = set(d[2],[26])

	c[2] = rotl(c[1] + F(d[2],a[2],b[1]) + m[6], 11)
	c[2] = eq(c[2],d[2],[13,15])
	c[2] = clear(c[2],[14,19,20,22])
	c[2] = set(c[2],[21])

	b[2] = rotl(b[1] + F(c[2],d[2],a[2]) + m[7], 19)
	b[2] = set(b[2],[13,14])
	b[2] = clear(b[2],[15,19,20,21,22])
	b[2] = eq(b[2],c[2],[17])
	
	a[3] = rotl(a[2] + F(b[2],c[2],d[2]) + m[8], 3)
	a[3] = set(a[3],[13,14,15,22])
	a[3] = clear(a[3],[17,19,20,21])
	a[3] = eq(a[3],b[2],[23,26])
	
	d[3] = rotl(d[2] + F(a[3],b[2],c[2]) + m[9], 7)
	d[3] = set(d[3],[13,14,15,21,22,26])
	d[3] = clear(d[3],[17,20,23])
	d[3] = eq(d[3],a[3],[30])
	
	c[3] = rotl(c[2] + F(d[3],a[3],b[2]) + m[10], 11)
	c[3] = set(c[3],[17,30])
	c[3] = clear(c[3],[20,21,22,23,26])
	c[3] = eq(c[3],d[3],[32])
	
	b[3] = rotl(b[2] + F(c[3],d[3],a[3]) + m[11], 19)
	b[3] = clear(b[3],[20,30,32])
	b[3] = set(b[3],[21,22,26])
	b[3] = eq(b[3],c[3],[23])
	
	a[4] = rotl(a[3] + F(b[3],c[3],d[3]) + m[12], 3)
	a[4] = clear(a[4],[23,26,32])
	a[4] = set(a[4],[30])
	a[4] = eq(a[4],b[3],[27,29])
	
	d[4] = rotl(d[3] + F(a[4],b[3],c[3]) + m[13], 7)
	d[4] = clear(d[4],[23,26,30])
	d[4] = set(d[4],[27,29,32])
	
	c[4] = rotl(c[3] + F(d[4],a[4],b[3]) + m[14], 11)
	c[4] = set(c[4],[23,26])
	c[4] = clear(c[4],[27,29,30])
	c[4] = eq(c[4],d[4],[19])
	
	b[4] = rotl(b[3] + F(c[4],d[4],a[4]) + m[15], 19)
	b[4] = clear(b[4],[19,30])
	b[4] = set(b[4],[26,27,29])
	
	m = get_m(a,b,c,d)
	
	#Multi-step message modification
	a[5] = rotl(a[4] + G(b[4],c[4],d[4]) + m[0] + 0x5A827999, 3)
	if bit(a[5],19) != bit(c[4],19):
		m[0] = (m[0]+(-1)**bit(a[5],19) * 2**15)%2**32
		a[5] = rotl(a[4] + G(b[4],c[4],d[4]) + m[0] + 0x5A827999, 3)
	if bit(a[5],26) == 0:
		m[0] = (m[0]+2**22)%2**32
		a[5] = rotl(a[4] + G(b[4],c[4],d[4]) + m[0] + 0x5A827999, 3)
	if bit(a[5],27) == 1:
		m[0] = (m[0]-2**23)%2**32
		a[5] = rotl(a[4] + G(b[4],c[4],d[4]) + m[0] + 0x5A827999, 3)
	if bit(a[5],29) == 0:
		m[0] = (m[0]+2**25)%2**32
		a[5] = rotl(a[4] + G(b[4],c[4],d[4]) + m[0] + 0x5A827999, 3)
	if bit(a[5],32) == 0:
		m[0] = (m[0]+2**28)%2**32
		a[5] = rotl(a[4] + G(b[4],c[4],d[4]) + m[0] + 0x5A827999, 3)
	
	a[1] = rotl(a[0] + F(b[0],c[0],d[0]) + m[0],3)
	d[1] = eq(d[1],a[1],[8,11])
	m = get_m(a,b,c,d)
	
	d[5] = rotl(d[4] + G(a[5],b[4],c[4]) + m[4] + 0x5A827999, 5)
	if bit(d[5],19) != bit(a[5],19):
		m[4] = (m[4]+(-1)**bit(d[5],19) * 2**13)%2**32
		d[5] = rotl(d[4] + G(a[5],b[4],c[4]) + m[4] + 0x5A827999, 5)
	if bit(d[5],26) != bit(b[4],26):
		m[4] = (m[4]+(-1)**bit(d[5],26) * 2**20)%2**32
		d[5] = rotl(d[4] + G(a[5],b[4],c[4]) + m[4] + 0x5A827999, 5)
	if bit(d[5],27) != bit(b[4],27):
		m[4] = (m[4]+(-1)**bit(d[5],27) * 2**21)%2**32
		d[5] = rotl(d[4] + G(a[5],b[4],c[4]) + m[4] + 0x5A827999, 5)
	if bit(d[5],29) != bit(b[4],29):
		m[4] = (m[4]+(-1)**bit(d[5],29) * 2**23)%2**32
		d[5] = rotl(d[4] + G(a[5],b[4],c[4]) + m[4] + 0x5A827999, 5)
	if bit(d[5],32) != bit(b[4],32):
		m[4] = (m[4]+(-1)**bit(d[5],32) * 2**26)%2**32
		d[5] = rotl(d[4] + G(a[5],b[4],c[4]) + m[4] + 0x5A827999, 5)

	a[2] = rotl(a[1] + F(b[1],c[1],d[1]) + m[4], 3)
	d[2] = eq(d[2],a[2],[19,20,21,22])
	m = get_m(a,b,c,d)
			
	#Create message with small differential
	m2 = [i for i in m]
	m2[1] += 2**31
	m2[2] += 2**31-2**28
	m2[12] += -2**16
	if md4.Round(a[0],b[0],c[0],d[0],m) == md4.Round(a[0],b[0],c[0],d[0],m2):
		return m,m2
	return None
	
def ct_success(f,n):
	ct = 0
	for i in range(n):
		if f():
			ct += 1
	return ct
	
def find_collision():
	ct = 0
	x = attempt()
	while not x:
		if ct%10000 == 0:
			print(ct)
		ct += 1
		x = attempt()
	return x,ct
	
def block2byte(l):
	ret = b""
	for i in l:
		ret += struct.pack(">I",i)
	return ret
	
def check_suff(m):
	a,b,c,d = [0]*13,[0]*13,[0]*13,[0]*13
	a[0],b[0],c[0],d[0] = 0x67452301,0xefcdab89,0x98badcfe,0x10325476

	a[1] = rotl(a[0] + F(b[0],c[0],d[0]) + m[0], 3)
	d[1] = rotl(d[0] + F(a[1],b[0],c[0]) + m[1], 7)
	c[1] = rotl(c[0] + F(d[1],a[1],b[0]) + m[2], 11)
	b[1] = rotl(b[0] + F(c[1],d[1],a[1]) + m[3], 19)
	a[2] = rotl(a[1] + F(b[1],c[1],d[1]) + m[4], 3)
	d[2] = rotl(d[1] + F(a[2],b[1],c[1]) + m[5], 7)
	c[2] = rotl(c[1] + F(d[2],a[2],b[1]) + m[6], 11)
	b[2] = rotl(b[1] + F(c[2],d[2],a[2]) + m[7], 19)
	a[3] = rotl(a[2] + F(b[2],c[2],d[2]) + m[8], 3)
	d[3] = rotl(d[2] + F(a[3],b[2],c[2]) + m[9], 7)
	c[3] = rotl(c[2] + F(d[3],a[3],b[2]) + m[10], 11)
	b[3] = rotl(b[2] + F(c[3],d[3],a[3]) + m[11], 19)
	a[4] = rotl(a[3] + F(b[3],c[3],d[3]) + m[12], 3)
	d[4] = rotl(d[3] + F(a[4],b[3],c[3]) + m[13], 7)
	c[4] = rotl(c[3] + F(d[4],a[4],b[3]) + m[14], 11)
	b[4] = rotl(b[3] + F(c[4],d[4],a[4]) + m[15], 19)
	a[5] = rotl(a[4] + G(b[4],c[4],d[4]) + m[0] + 0x5A827999, 3)
	d[5] = rotl(d[4] + G(a[5],b[4],c[4]) + m[4] + 0x5A827999, 5)
	c[5] = rotl(c[4] + G(d[5],a[5],b[4]) + m[8] + 0x5A827999, 9)
	
	old_a = [i for i in a]
	old_b = [i for i in b]
	old_c = [i for i in c]
	old_d = [i for i in d]
	
	a[1] = eq(a[1],b[0],[7])
	
	d[1] = clear(d[1],[7])
	d[1] = eq(d[1],a[1],[8,11])
	
	c[1] = set(c[1],[7,8])
	c[1] = clear(c[1],[11])
	c[1] = eq(c[1],d[1],[26])
	
	b[1] = set(b[1],[7])
	b[1] = clear(b[1],[8,11,26])
	
	a[2] = set(a[2],[8,11])
	a[2] = clear(a[2],[26])
	a[2] = eq(a[2],b[1],[14])
	
	d[2] = clear(d[2],[14])
	d[2] = eq(d[2],a[2],[19,20,21,22])
	d[2] = set(d[2],[26])
	
	c[2] = eq(c[2],d[2],[13,15])
	c[2] = clear(c[2],[14,19,20,22])
	c[2] = set(c[2],[21])
	
	b[2] = set(b[2],[13,14])
	b[2] = clear(b[2],[15,19,20,21,22])
	b[2] = eq(b[2],c[2],[17])
	
	a[3] = set(a[3],[13,14,15,22])
	a[3] = clear(a[3],[17,19,20,21])
	a[3] = eq(a[3],b[2],[23,26])
	
	d[3] = set(d[3],[13,14,15,21,22,26])
	d[3] = clear(d[3],[17,20,23])
	d[3] = eq(d[3],a[3],[30])
	
	c[3] = set(c[3],[17,30])
	c[3] = clear(c[3],[20,21,22,23,26])
	c[3] = eq(c[3],d[3],[32])
	
	b[3] = clear(b[3],[20,30,32])
	b[3] = set(b[3],[21,22,26])
	b[3] = eq(b[3],c[3],[23])
	
	a[4] = clear(a[4],[23,26,32])
	a[4] = set(a[4],[30])
	a[4] = eq(a[4],b[3],[27,29])
	
	d[4] = clear(d[4],[23,26,30])
	d[4] = set(d[4],[27,29,32])
	
	c[4] = set(c[4],[23,26])
	c[4] = clear(c[4],[27,29,30])
	c[4] = eq(c[4],d[4],[19])
	
	b[4] = clear(b[4],[19,30])
	b[4] = set(b[4],[26,27,29])
	
	a[5] = eq(a[5],c[4],[19])
	a[5] = set(a[5],[26,29,32])
	a[5] = clear(a[5],[27])
	
	d[5] = eq(d[5],a[5],[19])
	d[5] = eq(d[5],b[4],[26,27,29,32])
	
	return old_a == a and old_b == b and old_c == c and old_d == d
	