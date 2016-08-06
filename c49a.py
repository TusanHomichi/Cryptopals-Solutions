from matasano import *
import re

key = randbytes(16)
def parse(msg):
	global key
	if len(msg) != 3:
		print("Wrong message size")
		return False
	if not cbc_mac_verify(msg[0],key,msg[1],msg[2]):
		print("Bad mac")
		return False
	m = msg[0]
	src = ''
	dst = ''
	amt = 0
	for val in m.split(b'&'):
		p = val.split(b'=')
		if p[0] == b'from':
			src = p[1]
		elif p[0] == b'to':
			dst = p[1]
		elif p[0] == b'amount':
			if re.match(b"^[0-9]+.",p[1]):
				amt = int(p[1])
	print("Accepted transaction of %d from %s to %s" % (amt,src,dst))
	return True

account = str(randint(10**7,10**8-1))
victim = str(randint(10**7,10**8-1))

def generate(dst,amt):
	global account, key
	msg = "from=%s&to=%s&amount=%d" % (account,dst,amt)
	msg = bytes(msg.encode('ascii'))
	iv = randbytes(16)
	return (msg,iv,cbc_mac(msg,key,iv))
	
block1 = "from=%s&to" % account
block1 = bytes(block1.encode('ascii'))
new_block1 = "from=%s&to" % victim
new_block1 = bytes(new_block1.encode('ascii'))

msg,iv,mac = generate(account,1000000)
parse((new_block1 + msg[16:], xor(iv,xor(block1,new_block1)), mac))


