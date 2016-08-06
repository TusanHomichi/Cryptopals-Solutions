from matasano import *
from os import urandom

key = urandom(16)

def parse_token(tok):
	tok = pkcs7_unpad(aes_ecb_dec(tok,key))
	ret = {}
	for t in tok.split(b'&'):
		if t.count(ord('=')) != 1:
			return None
		t = t.split(b'=')
		ret[t[0]] = t[1]
	return ret
	
def generate_token(username):
	username = username.replace(b'&',b'').replace(b'=',b'')
	tok = b"email="+username+b"&uid=10&role=user"
	return aes_ecb_enc(pkcs7_pad(tok,16),key)
	
def make_admin():
	name = bytes([97]*10)+b"admin"+bytes([11]*11) + bytes([97]*3)
	tok = generate_token(name)
	bad_tok = tok[:16] + tok[32:-16] + tok[16:32]
	return bad_tok

print(parse_token(make_admin()))