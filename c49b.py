from matasano import *
import re

key = randbytes(16)
def parse(msg):
	global key
	if len(msg) != 2:
		print("Wrong message size")
		return False
	if not cbc_mac_verify(msg[0],key,b'\x00'*16,msg[1]):
		print("Bad mac")
		return False
	m = msg[0]
	src = ''
	tx = []
	for val in m.split(b'&'):
		k,v = val.split(b'=')
		if k == b'from':
			src = v
		elif k == b'tx_list':
			tx = v.split(b';')
	print("Accepted transaction from %s" % src)	
	for q in tx:
		a = q.split(b':')
		if re.match(b"^[0-9]+$",a[1]):
			print("\t$%s to %s" % (a[1],a[0]))
	return True

account = "Me"
victim = "Victim"

def generate(tx_list,src=account):
	global key
	msg = "from=%s&tx_list=%s:%d" % (src,tx_list[0][0],tx_list[0][1])
	for dst,amt in tx_list[1:]:
		msg += ";%s:%d" % (dst,amt)
	msg = bytes(msg.encode('ascii'))
	return (msg,cbc_mac(msg,key,b'\x00'*16))
	
cap_msg,cap_mac = generate([(randint(10**8),20)],src=victim)
msg,mac = generate([(account,100),(account,1000000)])
forge_msg = pkcs7_pad(cap_msg) + xor(cap_mac,msg[:16]) + msg[16:]
forge_mac = mac

parse((forge_msg,forge_mac))