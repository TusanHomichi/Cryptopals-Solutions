from matasano import *
from base64 import b64encode
import zlib
import string

secret = b64encode(randbytes(32))
def oracle(s):
	req = b"POST / HTTP/1.1\nHost: hapless.com\nCookie: sessionid=" + secret + b"\nContent-Length: " + bytes(str(len(s)).encode('ascii')) + b"\n" + s
	req = zlib.compress(req)
	key = randbytes(16)
	iv = randbytes(16)
	return aes_cbc_enc(pkcs7_pad(req),key,iv)
	
def outputs(x):
	lens = []
	for a in alph:
		l = len(oracle(x+bytes([a])))
		if l not in lens:
			lens.append(l)
	return lens
	
alph = string.ascii_letters+string.digits+"+/="
alph = alph.encode("ascii")
def get_sessionid():
	pref = b""
	while len(pref) < len(secret):
		#Find padding
		padding = 0
		while True:
			if len(outputs(b"a"*padding + b"sessionid=" + pref)) > 1:
				break
			padding += 1
		minLen = len(oracle(b"a"*padding + b"sessionid="+pref+b"a"))+1
		minChar = None
		for a in alph:
			l = len(oracle(b"a"*padding + b"sessionid="+pref+bytes([a])))
			if l < minLen:
				minLen = l
				minChar = a
		pref += bytes([minChar])
	return pref
	
assert(get_sessionid() == secret)
print("Got secret!")

